import httpx

import openai
from deepgram import Deepgram
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile, HTTPException

from app.config import DEEPGRAM_API_KEY
from app.routes.utils import send_message
from app.common.templates.url import js_code as url
from app.common.logging.loggers import file_logging
from app.services.utils.agent_util import generate_output
from app.services.selenium.webdriver import SingletonWebDriver
from app.services.langchain.callback import CustomCallbackHandler



deepgram = Deepgram(DEEPGRAM_API_KEY)

router = APIRouter()
singleton_webdriver = SingletonWebDriver()
driver = singleton_webdriver.get_driver()
driver.execute_script(url)

@router.post("/open_url", tags=["helper"])
async def open_url(url: str):
    driver.get(url)


@router.post("/bot", tags=["bot"])
async def bot(request: str):
    try:
        return await generate_output(request, CustomCallbackHandler())

    except openai.BadRequestError as e:
        file_logging.error(e)
        return HTTPException(status_code=429, detail="limit rate exceeded")

    except Exception as e:
        file_logging.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to generate output."
        )


@router.post("/upload_audio", tags=["helper"])
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    if not file_content:
        return JSONResponse(content={"error": "Empty file content"}, status_code=400)

    try:
        source = {"buffer": file_content, "mimetype": file.content_type}

        response = await deepgram.transcription.prerecorded(source, {"punctuate": True})
        response = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        print(response)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://127.0.0.1:8080/bot?request={response}"
            )
        return JSONResponse(content=response)
    except Exception as e:
        file_logging.error(e)
        return HTTPException(
            status_code=500, detail="Internal Server Error, failed to upload voice."
        )
