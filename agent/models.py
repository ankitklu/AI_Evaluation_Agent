from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    model="groq:openai/gpt-oss-20b",
    temperature=0
)

# response = model.invoke("Explain RAG in simple terms.")
# print(response.content)

