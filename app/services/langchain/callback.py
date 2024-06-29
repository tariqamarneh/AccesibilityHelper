import asyncio
from typing import Any, AsyncIterator, Dict, List, Literal, Union, cast


from langchain_core.outputs import LLMResult
from langchain.callbacks.base import AsyncCallbackHandler


class CustomCallbackHandler(AsyncCallbackHandler):
    queue: asyncio.Queue[str]
    done: asyncio.Event

    def __init__(self) -> None:
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        print("start")
        self.done.clear()

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        if token is not None and token != "":
            self.queue.put_nowait(token)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        print("end")
        self.done.set()

    async def aiter(self) -> AsyncIterator[str]:
        while not self.queue.empty() or not self.done.is_set():
            done, _ = await asyncio.wait(
                [
                    asyncio.ensure_future(self.queue.get()),
                    asyncio.ensure_future(self.done.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            token_or_done = cast(Union[str, Literal[True]], done.pop().result())

            if token_or_done is True:
                break

            yield token_or_done
