from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class TipoMovimentacao(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class MovimentacaoCreate(BaseModel):
    produto_id: UUID
    tipo: TipoMovimentacao
    quantidade: int = Field(..., gt=0)
    valor_unitario: float | None = Field(None, ge=0)

class MovimentacaoResponse(BaseModel):
    id: UUID
    usuario_id: UUID
    produto_id: UUID
    tipo: TipoMovimentacao
    quantidade: int
    valor_unitario: float | None
    data: datetime

    model_config = ConfigDict(from_attributes=True)