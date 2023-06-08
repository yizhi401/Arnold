#!/usr/bin/env python3

import os
import deeplake
import pathlib
import langchain
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain import LLMChain
from langchain.agents.agent import AgentExecutor


import tsprompt
import testdata
from testcase_generator.base import TestCaseGenerator

from langchain.memory import ConversationBufferMemory

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI


def initialise():
    langchain.verbose = True
    with open("keys/openai.key") as f:
        os.environ['OPENAI_API_KEY'] = f.read().strip()
    with open("keys/activeloop.key") as f:
        os.environ['ACTIVELOOP_TOKEN'] = f.read().strip()


def load_source2_vectorstore():
    root_dir = pathlib.Path(__file__).parent.parent / 'langchain' / 'langchain'
    docs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            try:
                loader = TextLoader(os.path.join(
                    dirpath, file), encoding='utf-8')
                docs.extend(loader.load_and_split())
            except Exception as e:
                pass

    embeddings = OpenAIEmbeddings(disallowed_special=())
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)
    username = "yizhi401"  # replace with your username from app.activeloop.ai
    # dataset would be publicly available
    db = DeepLake(dataset_path=f"hub://{username}/langchain-py",
                  embedding_function=embeddings, public=True)
    db.add_documents(texts)


def filter(x):
    # filter based on source code
    if 'com.google' in x['text'].data()['value']:
        return False

    # filter based on path e.g. extension
    metadata = x['metadata'].data()['value']
    return 'scala' in metadata['source'] or 'py' in metadata['source']


def run_query():
    qa = build_vectorstore_retriever()
    questions = [
        "What is the inheritance hierarchy for chain ?",
        # "What does favCountParams do?",
        # "is it Likes + Bookmarks, or not clear from the code?",
        # "What are the major negative modifiers that lower your linear ranking parameters?",
        # "How do you get assigned to SimClusters?",
        # "What is needed to migrate from one SimClusters to another SimClusters?",
        # "How much do I get boosted within my cluster?",
        # "How does Heavy ranker work. what are it’s main inputs?",
        # "How can one influence Heavy ranker?",
        # "why threads and long tweets do so well on the platform?",
        # "Are thread and long tweet creators building a following that reacts to only threads?",
        # "Do you need to follow different strategies to get most followers vs to get most likes and bookmarks per tweet?",
        # "Content meta data and how it impacts virality (e.g. ALT in images).",
        # "What are some unexpected fingerprints for spam factors?",
        # "Is there any difference between company verified checkmarks and blue verified individual checkmarks?",
    ]
    chat_history = []

    for question in questions:
        result = qa({"question": question, "chat_history": chat_history})
        chat_history.append((question, result['answer']))
        print(f"-> **Question**: {question} \n")
        print(f"**Answer**: {result['answer']} \n")


def build_vectorstore_retriever():
    embeddings = OpenAIEmbeddings(disallowed_special=())
    # ds = deeplake.load('hub://yizhi401/twitter-algorithm2')
    dataset = "hub://yizhi401/langchain-py"
    db = DeepLake(dataset_path=dataset,
                  read_only=True, embedding_function=embeddings)
    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos'
    retriever.search_kwargs['fetch_k'] = 100
    retriever.search_kwargs['maximal_marginal_relevance'] = True
    retriever.search_kwargs['k'] = 10
    # retriever.search_kwargs['filter'] = filter

    model = ChatOpenAI(model_name='gpt-3.5-turbo')  # switch to 'gpt-4'
    return ConversationalRetrievalChain.from_llm(
        model, retriever=retriever, verbose=True)


def build_testcase_chain():
    # prompt = PromptTemplate(
    #     template_format="jinja2",
    #     input_variables=["language", "test_libraries",
    #                      "desc", "related_codes", "code"],
    #     template=tsprompt.GENRAL_INSTRUCTION,
    # )
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    # llm_chain = LLMChain(
    #     prompt=prompt,
    #     llm=llm,
    # )
    tools = load_tools(["llm-math"], llm=llm)
    # tools = []
    agent_cls = TestCaseGenerator
    agent_obj = agent_cls.from_llm_and_tools(
        llm,
        tools,
        # input_variables=["input", "chat_history", "agent_scratchpad",
        #  "libraries"],
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    agent = AgentExecutor.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        memory=memory,
    )
    # agent_chain = initialize_agent(
    # tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

    # return agent_chain
    return agent


def buildup_langchain():
    # vschain = build_vectorstore_retriever()
    # testchain = build_testcase_chain()
    # print(testchain.run(**testdata.TEST_DATA))
    print(build_testcase_chain().run(input="""
```python
def add(x, y):
    return x + y
```
"""))


def main():
    initialise()
    # load_files()
    # load_source2_vectorstore()
    # run_query()
    buildup_langchain()


if __name__ == '__main__':
    main()
