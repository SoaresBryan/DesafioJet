from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from gemini.conexao_gemini import gerar_resposta

router = APIRouter()

class Mensagem(BaseModel):
    prompt: str

@router.post("/chat")
async def chat(mensagem: Mensagem, user_id: str = Header(...)):
    """
    Endpoint para interação com o chatbot.
    
    :param mensagem: Objeto contendo o prompt enviado pelo usuário.
    :param user_id: ID do usuário passado no cabeçalho.
    :return: Resposta gerada pela IA.
    """
    try:
        resposta = gerar_resposta(user_id, mensagem.prompt)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
