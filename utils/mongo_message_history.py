from langchain.schema import BaseChatMessageHistory
from langchain.schema import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)
from pymongo import MongoClient
import os
import logging
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["chatbot"]


class MongoDBMessageHistory(BaseChatMessageHistory):
    """
    Histórico de mensagens baseado em MongoDB para memória de conversação.

    Attributes:
        user_id (str): O ID do usuário.
        collection: A coleção MongoDB para o histórico de mensagens.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.collection = db["message_history"]

    @property
    def messages(self):
        """
        Recupera a lista de mensagens para o usuário.

        :return: Lista de objetos BaseMessage.
        """
        try:
            data = self.collection.find_one({"user_id": self.user_id})
            if data and "messages" in data:
                messages = []
                for msg in data["messages"]:
                    if msg["type"] == "human":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["type"] == "ai":
                        messages.append(AIMessage(content=msg["content"]))
                    elif msg["type"] == "system":
                        messages.append(SystemMessage(content=msg["content"]))
                    else:
                        messages.append(BaseMessage(content=msg["content"]))
                return messages
            else:
                return []
        except Exception as e:
            logging.error(f"Erro ao recuperar mensagens para o usuário {self.user_id}: {e}")
            raise

    def add_message(self, message: BaseMessage):
        """
        Adiciona uma mensagem ao histórico de mensagens do usuário.

        :param message: A mensagem a ser adicionada.
        """
        try:
            if isinstance(message, HumanMessage):
                msg_type = "human"
            elif isinstance(message, AIMessage):
                msg_type = "ai"
            elif isinstance(message, SystemMessage):
                msg_type = "system"
            else:
                msg_type = "base"

            self.collection.update_one(
                {"user_id": self.user_id},
                {"$push": {"messages": {"type": msg_type, "content": message.content}}},
                upsert=True
            )
        except Exception as e:
            logging.error(f"Erro ao adicionar mensagem para o usuário {self.user_id}: {e}")
            raise

    def clear(self):
        """
        Limpa o histórico de mensagens do usuário.
        """
        try:
            self.collection.delete_one({"user_id": self.user_id})
        except Exception as e:
            logging.error(f"Erro ao limpar mensagens para o usuário {self.user_id}: {e}")
            raise
