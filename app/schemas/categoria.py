from uuid import UUID
from pydantic import BaseModel, ConfigDict

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)