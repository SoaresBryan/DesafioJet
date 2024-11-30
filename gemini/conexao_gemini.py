
import os
import requests
import json
from dotenv import load_dotenv
from langchain.llms.base import LLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from typing import Optional, List
from utils.mongo_message_history import MongoDBMessageHistory

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-1.5-flash-latest:generateContent"
)

CONTEXT = (
    "Você é um vendedor de peças de computador, "
    "e sua tarefa é ajudar clientes a escolherem componentes de hardware "
    "de forma humanizada e amigável, sem enrolar muito. "
    "Se o usuário solicitar placas de vídeo, por exemplo, "
    "você já vai dizer alguns modelos que podem ser interessantes para ele. "
    "Responda de maneira clara e simpática, e sempre pergunte detalhes sobre "
    "a necessidade do cliente. Informe ao cliente que você é um chatbot humanizado. "
    "O horário de atendimento para que o cliente converse com humanos é de 08:00 "
    "da manhã até as 17:00. Quando o cliente falar da peça do computador que ele "
    "está desejando, você deve responder quanto ela custa e em seguida perguntar "
    "se ele tem interesse. Caso o cliente responda com algo similar a 'tenho interesse', "
    "sua tarefa então é passar essa conversa para um vendedor real. Você vai pedir "
    "para o cliente entrar em contato com o número de WhatsApp: 79 9 9996-66418. "
    "O preço médio da placa de vídeo é 1200 reais, do processador é 700, "
    "do gabinete é 300, da placa-mãe é 500 e da memória RAM 180."
)

class GeminiLLM(LLM):
    api_key: str
    endpoint: str

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(
            f"{self.endpoint}?key={self.api_key}",
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 200:
            result = response.json()
            try:
                resposta = result["candidates"][0]["content"]["parts"][0]["text"]
                return resposta
            except (KeyError, IndexError):
                raise Exception("Formato inesperado na resposta da API.")
        else:
            raise Exception(f"Erro {response.status_code}: {response.text}")

def gerar_resposta(user_id: str, prompt: str) -> str:
    """
    Gera uma resposta baseada no contexto do usuário e salva a interação.

    :param user_id: ID do usuário.
    :param prompt: Texto com a pergunta ou instrução.
    :return: Resposta gerada pela IA.
    """
    # Inicializa o LLM personalizado
    llm = GeminiLLM(api_key=GEMINI_API_KEY, endpoint=GEMINI_ENDPOINT)

    # Cria o histórico de mensagens do usuário
    message_history = MongoDBMessageHistory(user_id=user_id)

    # Adiciona o contexto como uma mensagem do sistema se for a primeira interação
    if not message_history.messages:
        message_history.add_message(SystemMessage(content=CONTEXT))

    # Configura a memória da conversa com o histórico do usuário
    memory = ConversationBufferMemory(
        chat_memory=message_history,
        return_messages=True
    )

    # Cria a cadeia de conversação sem um prompt personalizado
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )

    # Gera a resposta
    resposta = conversation.predict(input=prompt)

    return resposta
