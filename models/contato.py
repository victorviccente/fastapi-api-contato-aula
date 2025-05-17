from pydantic import BaseModel, EmailStr
from typing import Optional

class Contato(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str
    email: EmailStr
