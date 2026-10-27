from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date

load_dotenv()

logging.basicConfig(
    level= logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# (AI_Evaluation_Agent) (base) ankit.mishra@MP-MH26TH0205 AI_Evaluation_Agent % python3 agent/agent.py
# I would like to request a refund
# 2026-10-25 15:04:20,337 | INFO | HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# Sure, could you please provide your username so I can check your purchase history?
# reply : 
# user123
# 2026-10-25 15:04:32,527 | WARNING | Deserializing unregistered type objects.Answer from checkpoint. This will be blocked in a future version. Set LANGGRAPH_STRICT_MSGPACK=true to block now, or add to allowed_msgpack_modules to allow explicitly: [('objects', 'Answer')]
# 2026-10-25 15:04:33,093 | INFO | HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# 2026-10-25 15:04:33,099 | INFO | using get_user_purchase_history tool on user: user123
# 2026-10-25 15:04:33,636 | INFO | HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# 2026-10-25 15:04:33,642 | INFO | using the date tool
# 2026-10-25 15:04:34,494 | INFO | HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# Sure, could you let me know which item(s) you would like to refund? For example, the book, the pen, or both?
# reply : 
# both
# 2026-10-25 15:04:38,751 | INFO | HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# 2026-10-25 15:04:38,759 | INFO | using calculate_right_refund tool to get user's : user123 refund
# 2026-10-25 15:04:39,517 | INFO | HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# 2026-10-25 15:04:39,522 | INFO | using issue_refund_ticket for user: user123
# 2026-10-25 15:04:40,029 | INFO | HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# A refund ticket with the amount of 30 has been issued and should be arriving soon to your bank account.
# the job is done !

@tool
def get_user_purchase_history(user: str)-> dict:
    """this tool takes the user username and return a dict of the user purchase history if
    the user exists"""
    logging.info(f"using get_user_purchase_history tool on user: {user}")
    if users_data.get(user):
        return users_data[user]

    return {"status" : "there was no username found"}

@tool
def calculate_right_refund(user:str, items:list[PurchaseItem]) -> str:
    """this tool takes a list of the items to be returned and the username and
    will return how much the refund is worth"""

    logging.info(f"using calculate_right_refund tool to get user's : {user} refund")

    if users_data.get(user):
        total_refund = 0

        for item in items:
            if users_data[user].get(item.name):
                total_refund += users_data[user][item.name]["price"]

        return f"the value of the refund is: {total_refund}"

    return {"status": "there is no username found"}

@tool
def issue_refund_ticket(user:str, refund_amount: int) -> str:
    """this tool will send a ticket to the right team to return the refund"""

    logging.info(f"using issue_refund_ticket for user: {user}")

    return f"a refund ticket has been issued successfully with the amount of {refund_amount}"

@tool
def get_today_date(user:str) -> str:
    """Return today's date in YYYY-MM-DD format
    This tool takes no arguments
    only use if a user exist and an item is present for refund"""
    logging.info(f"using the date tool")
    return date.today().isoformat()

if __name__ == "__main__":
    book = PurchaseItem(name = "book")
    pen = PurchaseItem(name = "pen")
    print(get_user_purchase_history.invoke({"user":"user123", "items":[book, pen]}))

    print(issue_refund_ticket.invoke({"user":"user123","refund_amount":30}))
    print(get_today_date.invoke("user123"))


