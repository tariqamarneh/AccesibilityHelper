from fastapi import FastAPI
from deepgram import Deepgram
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.config import DEEPGRAM_API_KEY
from app.common.middleware.middleware import Middleware
from app.common.logging.loggers import file_logging
from app.routes.assistance import router as assistance_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    file_logging.info("Starting up...")
    yield
    file_logging.info("Shutting down...")


app = FastAPI(
    title="Accessibility helper API",
    summary="API for website accessibility helper for user.",
    description="API for website accessibility helper for user, using GPT-4o model to perform actions on the website based on user request using either text or voice.",
    version="0.1",
    openapi_tags=[
        {
            "name": "bot",
            "description": "Send a request to gpt4o to perform an action",
        },
        {
            "name": "helper",
            "description": "Helper methods to interact with the website.",
        },
    ],
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(Middleware)
app.include_router(assistance_router)

deepgram = Deepgram(DEEPGRAM_API_KEY)


@app.get("/")
async def root():
    return JSONResponse(content="Welcome to Accessibility Helper API's")


@app.get("/check_health")
async def check_health():
    return JSONResponse(content="Healthy")
