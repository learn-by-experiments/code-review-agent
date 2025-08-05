from langgraph.prebuilt import create_react_agent
from agents.llm import llm
from agents.prompt import query_gen_prompt


code_review_agent = create_react_agent(llm, [], prompt=query_gen_prompt)
