import os
import requests
import json
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da chave de API e endpoint
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Contexto inicial para a IA
CONTEXT = (
    "Você é um vendedor de peças de computador, "
    "e sua tarefa é ajudar clientes a escolherem componentes de hardware de forma humanizada e amigável. "
    "Responda de maneira clara e simpática, e sempre pergunte detalhes sobre a necessidade do cliente."
    "Exemplo:"
    "Cliente: Olá"
    "Vendedor: Olá! Tudo bem? Você está precisando de alguma peça de computador?"
    "Cliente: Sim, preciso de uma placa de vídeo."
    "Vendedor: Ótimo! Qual é a sua necessidade? Jogos mais leves ou mais pesados?"
)

def gerar_resposta(prompt: str) -> str:
    """
    Envia um prompt para a API do Gemini e retorna a resposta gerada.

    :param prompt: Texto com a pergunta ou instrução.
    :return: Resposta gerada pela IA.
    """
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"{CONTEXT}\nCliente: {prompt}\nVendedor:"}
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise Exception("Formato inesperado na resposta da API.")
    else:
        raise Exception(f"Erro {response.status_code}: {response.text}")
