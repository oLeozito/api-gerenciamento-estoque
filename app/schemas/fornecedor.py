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
    nome: str | None = Field(None, max_length=150)
    cnpj: str | None = Field(None, max_length=14)
    telefone: str | None = Field(None, max_length=20)
    email: EmailStr | None = None

class FornecedorListResponse(BaseModel):
    id: UUID
    nome: str
    cnpj: str
    
    model_config = ConfigDict(from_attributes=True)

class FornecedorDetailResponse(FornecedorBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)