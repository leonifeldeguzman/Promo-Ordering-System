import os
import asyncio
from livekit.agents import function_tool
from dotenv import load_dotenv
from groq import Groq

from livekit.agents import (
    Agent,
    AgentSession,
    WorkerOptions,
    cli,
)

from livekit.plugins import (
    deepgram,
    cartesia,
    silero,
)

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a fast food promo assistant."
        )

    async def on_user_turn(self, turn_ctx, new_message):
        user_text = new_message.content
        print("USER:", user_text)

        try:
            response = await asyncio.to_thread(
                groq_client.chat.completions.create,
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are a fast food promo assistant."},
                    {"role": "user", "content": user_text}
                ]
            )

            reply = response.choices[0].message.content
            print("AI:", reply)

            await turn_ctx.session.say(reply)

        except Exception as e:
            print("ERROR:", e)
            await turn_ctx.session.say("Sorry, I had an error.")

async def entrypoint(ctx):
    await ctx.connect()
    print("Agent connected to room!")

    agent = Assistant()

    session = AgentSession(
        agent=agent,
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3"),
        tts=cartesia.TTS(),
    )

    def on_turn_sync(turn_ctx, new_message):
        asyncio.create_task(agent.on_user_turn(turn_ctx, new_message))

    print("STT active")

    await session.start(room=ctx.room)

    print("Session started!")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name=os.getenv("AGENT_NAME", "promo-agent"),
        )
    )