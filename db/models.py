from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Interaction(BaseModel):
    user_id: str
    prompt: str
    response: str
    timestamp: datetime

class User(BaseModel):
    user_id: str
    interactions: Optional[List[Interaction]] = []
