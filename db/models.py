from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Interaction(BaseModel):
    """
    Modelo Pydantic representando uma interação do usuário.

    Attributes:
        user_id (str): O ID do usuário.
        prompt (str): A pergunta ou comando do usuário.
        response (str): A resposta da IA.
        timestamp (datetime): O timestamp da interação.
    """
    user_id: str
    prompt: str
    response: str
    timestamp: datetime


class User(BaseModel):
    """
    Modelo Pydantic representando um usuário.

    Attributes:
        user_id (str): O ID do usuário.
        interactions (Optional[List[Interaction]]): Lista de interações do usuário.
    """
    user_id: str
    interactions: Optional[List[Interaction]] = []
