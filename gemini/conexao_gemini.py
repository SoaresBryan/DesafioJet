import os
import requests
import json
import logging
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
    "Você é um vendedor especializado em componentes de computadores e representa exclusivamente a loja JetSales. "
    "Sua principal tarefa é ajudar os clientes a escolherem os melhores componentes de hardware com base em suas necessidades específicas, "
    "garantindo que a experiência de compra seja prática, amigável e confiável. "
    "É extremamente importante que você nunca recomende que o cliente procure outro lugar ou loja para comprar o produto. "
    "Todos os produtos devem ser apresentados como disponíveis na JetSales, com a opção de finalizar a compra diretamente com um vendedor humano, caso o cliente demonstre interesse. "
    "Se o cliente mencionar interesse em qualquer produto, você deve informá-lo de forma educada que ele pode entrar em contato com um vendedor humano da JetSales "
    "pelo WhatsApp no número 79 9 9996-66418 para concluir a compra ou tirar dúvidas específicas. Nunca insinue que ele procure outra loja ou fornecedor. "
    "Ao interagir com o cliente, seja direto, simpático e humanizado, mas evite começar todas as respostas com 'Olá' ou 'Oi'. "
    "Você só deve usar saudações como 'Olá' ou 'Oi, tudo bem?' na primeira interação com o cliente. "
    "Se o cliente mencionar algum componente de computador, responda com recomendações específicas, incluindo modelos e preços médios."
    "Explique por que o produto é ideal para o cliente com base em suas necessidades. "
    "Pergunte detalhes como: 'É para jogos pesados ou tarefas do dia a dia?' ou 'Qual é a sua prioridade: desempenho ou custo-benefício?'. "
    "Nunca ofereça o contato de um vendedor humano automaticamente. "
    "Você só deve passar o contato de um vendedor humano se o cliente expressar explicitamente interesse com frases como: "
    "'Tenho interesse', 'Quero falar com um humano' ou 'Quero saber mais'. "
    "Caso o cliente pergunte algo fora do horário comercial (08:00 às 17:00), avise-o educadamente sobre o horário de atendimento humano. "
    "Deixe claro que você é um chatbot humanizado da JetSales e que pode ajudá-lo no que for necessário dentro de suas limitações. "
    "Seu objetivo é fornecer respostas úteis, informativas e amigáveis, sempre reforçando que os produtos estão disponíveis exclusivamente na JetSales. "
    "Adapte-se ao contexto da conversa, mostrando entusiasmo, conhecimento e compromisso com a solução das necessidades do cliente."
)


class GeminiLLM(LLM):
    """
    Classe LLM personalizada para interagir com a API do Gemini.

    Attributes:
        api_key (str): Chave de API para o Gemini.
        endpoint (str): URL do endpoint da API do Gemini.
    """
    api_key: str
    endpoint: str

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Faz uma chamada para a API do Gemini com o prompt fornecido.

        :param prompt: O prompt ou pergunta a ser enviada para a API.
        :param stop: Lista opcional de sequências de parada.
        :return: Texto da resposta da API.
        :raises Exception: Se houver um erro na resposta da API.
        """
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

        try:
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
                except (KeyError, IndexError) as e:
                    logging.error(f"Formato inesperado na resposta da API: {e}")
                    raise Exception("Formato inesperado na resposta da API.")
            else:
                logging.error(f"Erro da API {response.status_code}: {response.text}")
                raise Exception(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            logging.error(f"Erro ao chamar a API Gemini: {e}")
            raise


def gerar_resposta(user_id: str, prompt: str) -> str:
    """
    Gera uma resposta baseada no contexto do usuário e salva a interação.

    :param user_id: ID do usuário.
    :param prompt: Texto com a pergunta ou instrução.
    :return: Resposta gerada pela IA.
    """
    try:
        llm = GeminiLLM(api_key=GEMINI_API_KEY, endpoint=GEMINI_ENDPOINT)

        # Cria o histórico de mensagens do usuário
        message_history = MongoDBMessageHistory(user_id=user_id)

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

        resposta = conversation.predict(input=prompt)

        return resposta
    except Exception as e:
        logging.error(f"Erro ao gerar resposta para o usuário {user_id}: {e}")
        raise
