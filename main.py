# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routers import chat

app = FastAPI(
    title="Chatbot com FastAPI e Gemini",
    description="API para interação com o chatbot utilizando o modelo Gemini.",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/api", tags=["Chat"])

# Monta o diretório 'static' para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para servir o index.html
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)
