from fastapi import FastAPI
from routers import chat

app = FastAPI(
    title="Chatbot com FastAPI e Gemini",
    description="API para interação com o chatbot utilizando o modelo Gemini.",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/api", tags=["Chat"])
