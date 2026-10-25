from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ProdutoBase(BaseModel):
    nome: str = Field(..., max_length=150)
    codigo: str = Field(..., max_length=150)
    descricao: str | None = Field(None, max_length=600)
    preco_custo: float = Field(..., ge=0) 
    preco_venda: float = Field(..., ge=0)
    categoria_id: UUID
    fornecedor_id: UUID

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, max_length=150)
    codigo: str | None = Field(None, max_length=150)
    descricao: str | None = Field(None, max_length=600)
    preco_custo: float | None = Field(None, ge=0)
    preco_venda: float | None = Field(None, ge=0)
    categoria_id: UUID | None = None
    fornecedor_id: UUID | None = None
    qtd_estoque: int | None = Field(None, ge=0)

class ProdutoListResponse(BaseModel):
    id: UUID
    codigo: str
    nome: str
    descricao: str | None
    qtd_estoque: int
    
    model_config = ConfigDict(from_attributes=True)

class ProdutoDetailResponse(ProdutoBase):
    id: UUID
    qtd_estoque: int 

    model_config = ConfigDict(from_attributes=True)