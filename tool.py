import logging
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
    
    transfer_to = "tel:+916302152129"
    
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