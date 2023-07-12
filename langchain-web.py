import os
from dotenv import load_dotenv, find_dotenv

from langchain import LLMChain, OpenAI
from langchain.chat_models import ChatOpenAI


load_dotenv(find_dotenv(), override=True)
chat_llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')


from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool, DuckDuckGoSearchRun
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

search = DuckDuckGoSearchRun()
searchTool = Tool(name="search", func=search.run, description="useful for when you need answers about current events. Should be asked targeted, concise questions")

memory = ConversationBufferWindowMemory(memory_key='chat_history', k=3, return_messages=True)

conversational_agent = initialize_agent(
    agent="chat-conversational-react-description",
    tools = [searchTool],
    llm = chat_llm,
    verbose = True,
    max_iterations = 3,
    early_stopping_method = "generate",
    memory = memory
)

prompt_to_use_tools = '''Assistant is a large language model trained by OpenAI.
Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
Assistant doesn't know anything about current events, and should use a tool for questions about these topics.
Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.'''

conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = prompt_to_use_tools


conversational_agent("What happned to the Nova Scotia RCMP today?")