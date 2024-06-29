from langchain_openai import AzureChatOpenAI

from app.config import AZURE_ENDPOINT, OPENAI_API_KEY


def get_llm(callback) -> AzureChatOpenAI:
    azure_llm = AzureChatOpenAI(
        deployment_name="gpt4o",
        azure_endpoint=AZURE_ENDPOINT,
        openai_api_key=OPENAI_API_KEY,
        api_version="2024-02-15-preview",
        temperature=0,
        # model='gpt-4o'
        # streaming=True,
        # callbacks=[callback]
    )
    return azure_llm
