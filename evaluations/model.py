import os
from dotenv import load_dotenv
from deepeval.models import GeminiModel

load_dotenv()

# Gemini free tier as the judge; Groq's free 8k TPM limit is too small for task-completion traces
eval_model = GeminiModel(
    model="gemini-3.8-flash",
    api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
    temperature=0
)
