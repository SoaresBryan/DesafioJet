from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from gemini.conexao_gemini import gerar_resposta

router = APIRouter()

class Mensagem(BaseModel):
    prompt: str

@router.post("/chat")
async def chat(mensagem: Mensagem):
    """
    Endpoint para interação com o chatbot.
    
    :param mensagem: Objeto contendo o prompt enviado pelo usuário.
    :return: Resposta gerada pela IA.
    """
    try:
        resposta = gerar_resposta(mensagem.prompt)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
