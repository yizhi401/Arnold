import os
import openai
with open("keys/openai.key") as f:
    openai.api_key = f.read().strip()

content = """
Answer the following questions as best you can. You have access to the following tools:

Search: A search engine. Useful for when you need to answer questions about current events. Input should be a search que
ry.
Calculator: Useful for when you need to answer questions about math.


Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [Search, Calculator]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

When taking an action, don't makeup the result of the action. Stops at Action and Action Input, I will fill in the Observation.

Begin!

Question: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?
Thought:
"""
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "user", "content": content}
    ]
)

print(completion.choices[0].message['content'])
