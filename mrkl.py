
import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
import langchain


def main():
    with open("keys/openai.key") as f:
        os.environ['OPENAI_API_KEY'] = f.read().strip()
    with open("keys/serpapi.key") as f:
        os.environ["SERPAPI_API_KEY"] = f.read().strip()
    langchain.verbose = True

    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent.run(
        "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")


if __name__ == '__main__':
    main()
