from fastapi import APIRouter, HTTPException, Header
from gemini.conexao_gemini import gerar_resposta
import logging

router = APIRouter()


@router.post("/chat")
async def chat(mensagem: str, user_id: str = Header(...)):
    """
    Endpoint para interação com o chatbot.

    :param mensagem: String contendo o prompt enviado pelo usuário.
    :param user_id: ID do usuário passado no cabeçalho.
    :return: Resposta gerada pela IA.
    """
    try:
        logging.info(f"Recebido user_id: {user_id}")
        logging.info(f"Recebido prompt: {mensagem}")

        resposta = gerar_resposta(user_id, mensagem)
        return resposta 

    except Exception as e:
        logging.error(f"Erro no endpoint /chat para o usuário {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
