import os
import sys
import langchain
from dotenv import load_dotenv, find_dotenv
from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.chains.summarize import load_summarize_chain
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.utilities import WikipediaAPIWrapper
from langchain import PromptTemplate

load_dotenv(find_dotenv(), override=True)
key = os.environ.get("OPEN_AI_LANG")

template = '''You are a {role}. Write a few sentences about {topic}.'''
prompt = PromptTemplate(
    input_variables=['role', 'topic'],
    template=template
)


## Text Completion Model
text = OpenAI(openai_api_key=key, model_name='text-davinci-003', temperature=0.7, max_tokens=256)
# text.get_num_tokens(message)
# resp = text.generate(["What color is the sky?", "How many are in a baker's dozen?"])
# resp = text("What are some simple colour grading techniques?")


# resp = text(prompt.format(role=sys.argv[1], topic=sys.argv[2]))




## Chat Model
chat = ChatOpenAI(openai_api_key=key, model_name='gpt-3.5-turbo', temperature=0.7, max_tokens=256)
# messages = [
#     SystemMessage(content="You are a content creator on instagram"),
#     HumanMessage(content="Explain what you do in a day")
# ]

# chain = LLMChain(llm=chat, prompt=prompt)
# resp = chain.run({'role': sys.argv[1], 'topic': sys.argv[2]})




## Simple Sequential Chains - only 1 input, 1 output per node
# prompt1 = PromptTemplate(
#     input_variables=['function'],
#     template='''Write python code to {function}'''
# )

# prompt2 = PromptTemplate(
#     input_variables=['fn'],
#     template='''Given the function {fn}, describe it to a novice student.'''
# )

# chain1 = LLMChain(llm=text, prompt=prompt1)
# chain2 = LLMChain(llm=chat, prompt=prompt2)
# overallChain = SimpleSequentialChain(chains=[chain1, chain2])
# resp = overallChain.run(sys.argv[1])




## LangChain Agents
code = OpenAI(openai_api_key=key, model_name='text-davinci-003', temperature=0)
# agentExecutor = create_python_agent(llm=code, tool=PythonREPLTool())
# resp = agentExecutor.run('What is the magnitude of (33 + 37i)')


# with open('data/threads.txt') as f:
#     threads_data = f.read()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 100,
#     chunk_overlap= 20,
#     length_function= len
# )

# chunks = text_splitter.create_documents([threads_data])
# print(len(chunks))



# def load_from_wikipedia(query, lang='en'):
#     from langchain.document_loaders import WikipediaLoader
#     loader = WikipediaLoader(query=query, lang=lang, load_max_docs=3)
#     return loader.load()

# data = load_from_wikipedia('Threads (App)')
# print(data[0].page_content)
summarizer = ChatOpenAI(openai_api_key=key, model_name='gpt-3.5-turbo', temperature=0)


wikipedia = WikipediaAPIWrapper()
tools = [
    Tool(name="Wikipedia", func=wikipedia.run, description='Get information from wikipedia')
]

wikiAgent = initialize_agent(tools, summarizer, agent='zero-shot-react-description', verbose=True)
resp = wikiAgent.run('Provide me a summary of Threads (app)')


## Summarizing From Templates
summarizer = ChatOpenAI(openai_api_key=key, model_name='gpt-3.5-turbo', temperature=0)

# summaryTemplate = '''Write a concise summary of the following as a pirate: TEXT: `{text}` CONCISE SUMMARY:'''
# summaryPrompt = PromptTemplate(input_variables=['text'], template=summaryTemplate)

# combineTemplate = '''
# Write a concise summary of the following.
# Text: `{text}`
# '''
# combinePrompt = PromptTemplate(input_variables=['text'], template=combineTemplate)

# with open('data/threads.txt') as f:
#     threads_data = f.read()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 3000,
#     chunk_overlap= 20,
#     length_function= len
# )
# chunks = text_splitter.create_documents([threads_data])

# # chain = load_summarize_chain(llm=summarizer, chain_type='map_reduce', verbose=True)
# # resp = chain.run(chunks)

# pirateChain = load_summarize_chain(llm=summarizer, chain_type='map_reduce', map_prompt=summaryPrompt, combine_prompt=combinePrompt, verbose=True)
# resp = pirateChain.run(chunks)





print(resp)