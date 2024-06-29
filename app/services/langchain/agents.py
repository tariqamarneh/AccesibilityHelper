from langchain.agents import AgentExecutor
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.langchain.tools import tools
from app.services.langchain.llms import get_llm
from app.services.prompt.assistance_prompt import prompt


async def agent_executor(callback) -> AgentExecutor:
    azure_llm = get_llm(callback)
    llm_with_tools = azure_llm.bind_tools(tools)
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
