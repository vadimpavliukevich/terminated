from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from tools import get_linux_command

llm = ChatOpenAI(temperature=0)

@tool
def get_linux_command_wrapper(command: str) -> str:
    """Wrapper for the get_linux_command function."""
    return get_linux_command(command)


tools = [get_linux_command_wrapper]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a very powerful assistant that helps the user to navigate the linux system."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm_with_tools = llm.bind(
    functions=[format_tool_to_openai_function(t) for t in tools]
)

agent = {
    "input": lambda x: x["input"],
    "agent_scratchpad": lambda x: format_to_openai_functions(x['intermediate_steps'])
} | prompt | llm_with_tools | OpenAIFunctionsAgentOutputParser()

agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)


def run_agent(user_input):
    """Invoke the agent executor with the given input."""
    return agent_executor.invoke({"input": user_input})

