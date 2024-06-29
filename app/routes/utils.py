import asyncio
from typing import AsyncIterable, Awaitable

from langchain.agents import AgentExecutor
from langchain.callbacks import AsyncIteratorCallbackHandler

from app.common.logging.loggers import file_logging
from app.services.langchain.agents import agent_executor
from app.services.utils.agent_util import generate_output
from app.services.langchain.callback import CustomCallbackHandler


agent: AgentExecutor = agent_executor


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    try:
        await fn
    except Exception as e:
        file_logging.error(e)
    finally:
        event.set()


async def send_message(msg: str) -> AsyncIterable[any]:
    callback = CustomCallbackHandler()
    task = asyncio.create_task(
        wrap_done(
            generate_output(question=msg, callback=callback),
            callback.done,
        )
    )
    async for token in callback.aiter():
        print(f"Received: |{token}|")
        yield token

    await task
