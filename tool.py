import os
import logging
import asyncio
import phonenumbers
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from phonenumbers import NumberParseException

from livekit import api
from livekit.agents import function_tool, RunContext, get_job_context


@function_tool
async def transfer_to_human(ctx: RunContext) -> str:
    """Transfer to specialist. Call only after confirming the users name and consent to be transferred."""
    logger = logging.getLogger("phone-assistant")
    job_ctx = get_job_context()
    
    if job_ctx is None:
        logger.error("Job context not found")
        return "error"
    
    transfer_to = "tel:+17328633049"
    
    # Find SIP participant
    sip_participant = None
    for participant in job_ctx.room.remote_participants.values():
        if participant.identity.startswith("sip:"):
            sip_participant = participant
            break
    
    if sip_participant is None:
        logger.error("No SIP participant found")
        return "error"
    
    logger.info(f"Transferring call for participant {sip_participant.identity} to {transfer_to}")
    
    try:
        await job_ctx.api.sip.transfer_sip_participant(
            api.TransferSIPParticipantRequest(
                room_name=job_ctx.room.name,
                participant_identity=sip_participant.identity,
                transfer_to=transfer_to,
                play_dialtone=True
            )
        )
        logger.info(f"Successfully transferred participant {sip_participant.identity} to {transfer_to}")
        return "transferred"
    except Exception as e:
        logger.error(f"Failed to transfer call: {e}", exc_info=True)
        return "error"


@function_tool
async def end_call(ctx: RunContext) -> str:
    """End call. If the user isn't interested, expresses general disinterest or wants to end the call"""
    logger = logging.getLogger("phone-assistant")
    job_ctx = get_job_context()
    
    if job_ctx is None:
        logger.error("Failed to get job context")
        return "error"
    
    logger.info(f"Ending call for room {job_ctx.room.name}")
    
    try:
        await job_ctx.api.room.delete_room(
            api.DeleteRoomRequest(
                room=job_ctx.room.name,
            )
        )
        logger.info(f"Successfully ended call for room {job_ctx.room.name}")
        return "ended"
    except Exception as e:
        logger.error(f"Failed to end call: {e}", exc_info=True)
        return "error"


def normalize_phone(raw: str, default_region: str = "IN") -> Optional[str]:
    """Validate and normalize a phone number to E.164 format.
    
    Args:
        raw: The raw phone number string to validate
        default_region: Default region code (ISO 3166-1 alpha-2) for numbers without country code
        
    Returns:
        str: Normalized phone number in E.164 format, or None if invalid
    """
    try:
        parsed = phonenumbers.parse(raw, default_region)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(
                parsed, 
                phonenumbers.PhoneNumberFormat.E164
            )
    except NumberParseException:
        pass
    return None

async def make_call(phone_number: str, room_name: Optional[str] = None) -> bool:
    """Make an outbound call to the specified phone number.
    
    Args:
        phone_number: The phone number to call (include country code, e.g., +1234567890)
        room_name: Optional room name. If not provided, a random one will be generated.
        
    Returns:
        bool: True if the call was initiated successfully, False otherwise
    """
    logger = logging.getLogger("phone-assistant")
    load_dotenv(Path(__file__).parent / '.env')
    
    # Validate and normalize the phone number
    normalized_number = normalize_phone(phone_number)
    if not normalized_number:
        logger.error(f"Invalid phone number: {phone_number}")
        return False
    
    # Get SIP trunk ID from environment
    sip_trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")
    if not sip_trunk_id or not sip_trunk_id.startswith("ST_"):
        logger.error("SIP_OUTBOUND_TRUNK_ID is not set or invalid")
        return False
    
    # Generate a room name if not provided
    if not room_name:
        room_name = f"outbound-call-{os.urandom(4).hex()}"
    
    lkapi = None
    try:
        lkapi = api.LiveKitAPI()
        
        # Create agent dispatch with normalized phone number as metadata
        logger.info(f"Creating dispatch in room {room_name} for {normalized_number}")
        dispatch = await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name="in&out",  # Must match the agent_name in agent.py
                room=room_name,
                metadata=normalized_number  # Use the normalized number
            )
        )
        logger.info(f"Created dispatch: {dispatch}")

        # Create SIP participant to make the call
        logger.info(f"Dialing {normalized_number} to room {room_name}")
        sip_participant = await lkapi.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=room_name,
                sip_trunk_id=sip_trunk_id,
                sip_call_to=normalized_number,
                participant_identity=f"phone-{normalized_number}"
            )
        )
        logger.info(f"Created SIP participant: {sip_participant}")
        return True
        
    except Exception as e:
        logger.error(f"Error during outbound call: {e}", exc_info=True)
        return False
    finally:
        if lkapi:
            await lkapi.aclose()

@function_tool
async def initiate_call(phone_number: str) -> str:
    """Initiate an outbound call to the specified phone number.
    
    Args:
        phone_number: The phone number to call (include country code, e.g., +1234567890)
        
    Returns:
        str: Status message indicating success or failure
    """
    success = await make_call(phone_number)
    return "Call initiated successfully" if success else "Failed to initiate call"