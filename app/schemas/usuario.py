from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
import re

class UsuarioLogin(BaseModel):
    usuario: str
    senha: str

class UsuarioCreate(BaseModel):
    nome: str
    usuario: str
    cargo: str = "estoquista"

    senha: str

    @field_validator('senha')
    @classmethod
    def validar_senha_forte(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('A senha deve ter no mínimo 8 caracteres.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('A senha deve ter pelo menos uma letra maiúscula.')
        if not re.search(r'[a-z]', v):
            raise ValueError('A senha deve ter pelo menos uma letra minúscula.')
        if not re.search(r'\d', v):
            raise ValueError('A senha deve ter pelo menos um número.')
        if not re.search(r'[\W_]', v): # \W pega qualquer caractere especial/símbolo
            raise ValueError('A senha deve ter pelo menos um caractere especial.')
        return v

class UsuarioResponse(BaseModel):
    id: UUID
    nome: str
    usuario: str
    cargo: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)