import os
import logging
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.agents.voice.room_io import RoomOptions, AudioInputOptions
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import mistralai
from prompt import AGENT_INSTRUCTIONS, SESSION_INSTRUCTIONS, OUTBOUND_AGENT_INSTRUCTIONS, OUTBOUND_SESSION_INSTRUCTIONS
from tool import transfer_to_human, end_call, initiate_call

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self, is_outbound: bool = False):
        self.is_outbound = is_outbound
        instructions = OUTBOUND_AGENT_INSTRUCTIONS if is_outbound else AGENT_INSTRUCTIONS
        super().__init__(
            instructions=instructions,
            tools=[transfer_to_human, end_call, initiate_call]
        )


async def entrypoint(ctx: agents.JobContext):
    # Set up logging
    logger = logging.getLogger("outbound-agent")
    
    # Check if this is an outbound call by looking for phone number in metadata
    is_outbound = bool(getattr(ctx, 'metadata', None) and ctx.metadata.startswith('+'))
    
    if is_outbound:
        logger.info(f"Starting outbound call to {ctx.metadata}")
    else:
        logger.info("Starting inbound call")
    
    session = AgentSession(
        stt="deepgram/nova-3:en",
        llm=mistralai.LLM(model="mistral-small-2506"),
        tts="elevenlabs/eleven_turbo_v2_5:Xb7hH8MSUJpSbSDYk0k2",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(is_outbound=is_outbound),
        room_options=RoomOptions(
            audio_input=AudioInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        ),
    )

    # Use appropriate instructions based on call direction
    instructions = OUTBOUND_SESSION_INSTRUCTIONS if is_outbound else SESSION_INSTRUCTIONS
    await session.generate_reply(instructions=instructions)
    
    if is_outbound:
        logger.info(f"Outbound call to {ctx.metadata} is active")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="in&out"
    ))