from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routers import chat
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI(
    title="Chatbot com FastAPI e Gemini",
    description="API para interação com o chatbot utilizando o modelo Gemini.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["Chat"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """
    Serve a página index.html.

    :return: O conteúdo de index.html como um HTMLResponse.
    """
    try:
        with open("static/index.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        logging.error(f"Erro ao servir index.html: {e}")
        return HTMLResponse(content="Erro ao carregar a página.", status_code=500)
