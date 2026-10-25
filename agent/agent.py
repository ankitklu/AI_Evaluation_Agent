from models import model
from tools import calculate_right_refund, get_user_purchase_history, get_today_date, issue_refund_ticket
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.agents.middleware import ModelRetryMiddleware
from objects import Answer
from prompts import agent_system_prompt
from langgraph.checkpoint.memory import InMemorySaver

from langchain.messages import HumanMessage

from uuid import uuid4

load_dotenv()

agent = create_agent(
    model = model,
    system_prompt= agent_system_prompt,
    tools = [calculate_right_refund, get_user_purchase_history, get_today_date, issue_refund_ticket],
    response_format=ToolStrategy(Answer),
    checkpointer= InMemorySaver(),
    # groq + gpt-oss occasionally emits a malformed tool call (400 output_parse_failed); retrying usually succeeds
    middleware=[ModelRetryMiddleware(max_retries=3, retry_on=lambda e: "output_parse_failed" in str(e), on_failure="error")]
)

def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}

    text = "I would like to request a refund"
    print(text)

    question = HumanMessage(content=text)
    
    conversation = True

    while conversation:

        response = agent.invoke({"messages": question}, config=config)
        structured_response = response["structured_response"]

        print(structured_response.answer)

        conversation = structured_response.conversation

        if conversation:
            user_input = input("reply : \n")
            question = HumanMessage(content=user_input)


    print("the job is done !")

run_conversation()