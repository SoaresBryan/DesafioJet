from langchain.schema import BaseChatMessageHistory
from langchain.schema import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["chatbot"]


class MongoDBMessageHistory(BaseChatMessageHistory):
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.collection = db["message_history"]

    @property
    def messages(self):
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

    def add_message(self, message: BaseMessage):
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

    def clear(self):
        self.collection.delete_one({"user_id": self.user_id})
