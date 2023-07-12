import os
from dotenv import load_dotenv, find_dotenv

from langchain import LLMChain, OpenAI
from langchain.chat_models import ChatOpenAI


load_dotenv(find_dotenv(), override=True)
chat_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool, DuckDuckGoSearchRun
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import urllib.request
from bs4 import BeautifulSoup

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="useful for when you need answers about current events. Should be asked targeted, concise questions",
)


class WebPageTool(BaseTool):
    name = "Get Webpage"
    description = "Useful for when you need to get specific types of content from a specific webpage"

    def _run(self, webpage: str):
        webUrl = urllib.request.urlopen(webpage)
        if webUrl.code == 200:
            htmldata = webUrl.read()
            soup = BeautifulSoup(htmldata, "html.parser")

            # if content_type=="text":
            content = soup.get_text()
            content = content.replace('\n', '')
            if len(content)>5000:
                content = content[:5000]
            # else:
            #     content = soup.find_all(content_type)
            
            return content
        
        return "Website could not be reached"
    
    def _arun(self, webpage: str):
        raise NotImplementedError("Tool does not support async")
    
webpage_tool = WebPageTool()


memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=3, return_messages=True
)

conversational_agent = initialize_agent(
    agent="chat-conversational-react-description",
    tools=[search_tool, webpage_tool],
    llm=chat_llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method="generate",
    memory=memory,
)

prompt_to_use_tools = """Assistant is a large language model trained by OpenAI.
Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
Assistant doesn't know anything about current events, and should use a search tool for questions about these topics.
Assistant doesn't know anything about the contents of specific webpages, and should use the 'Get Webpage' tool for questions about these topics.
Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist."""

conversational_agent.agent.llm_chain.prompt.messages[0].prompt.template = prompt_to_use_tools


conversational_agent("What are the top stories on CBS news?")
