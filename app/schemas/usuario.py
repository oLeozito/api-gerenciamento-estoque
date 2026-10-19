from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UsuarioLogin(BaseModel):
    usuario: str
    senha: str

class UsuarioCreate(BaseModel):
    nome: str
    usuario: str
    senha: str
    cargo: str = "estoquista"

class UsuarioResponse(BaseModel):
    id: UUID
    nome: str
    usuario: str
    cargo: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)