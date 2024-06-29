from langchain.agents import AgentExecutor

from app.common.templates.chat import js_code
from app.services.langchain.agents import agent_executor
from app.services.selenium.webdriver import SingletonWebDriver

singleton_webdriver = SingletonWebDriver()
driver = singleton_webdriver.get_driver()


async def generate_output(question, callback):
    agent: AgentExecutor = await agent_executor(callback)
    response = await agent.ainvoke({"input": question})
    return response["output"]
