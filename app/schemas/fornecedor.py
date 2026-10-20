from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class FornecedorBase(BaseModel):
    nome: str = Field(..., max_length=150)
    cnpj: str = Field(..., max_length=14)
    telefone: str = Field(..., max_length=20)
    email: EmailStr

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(BaseModel):
    # Todos os campos são opcionais para o PATCH/PUT, permitindo atualizar apenas um dado por vez
    nome: str | None = Field(None, max_length=150)
    cnpj: str | None = Field(None, max_length=14)
    telefone: str | None = Field(None, max_length=20)
    email: EmailStr | None = None

class FornecedorListResponse(BaseModel):
    # O filtro perfeito: o Pydantic só deixará passar esses três campos
    id: UUID
    nome: str
    cnpj: str
    
    model_config = ConfigDict(from_attributes=True)

class FornecedorDetailResponse(FornecedorBase):
    # Inclui nome, cnpj, telefone, email (herdados) + id
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)