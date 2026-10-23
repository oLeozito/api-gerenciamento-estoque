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
    quantidade: int = Field(..., gt=0) # gt=0 garante que a quantidade seja maior que zero

class MovimentacaoResponse(BaseModel):
    id: UUID
    produto_id: UUID
    tipo: TipoMovimentacao
    quantidade: int
    data: datetime

    model_config = ConfigDict(from_attributes=True)