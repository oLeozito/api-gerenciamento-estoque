from pydantic import BaseModel
from uuid import UUID
from datetime import date

class ProdutoVendaResp(BaseModel):
    id: UUID
    nome: str
    quantidade_vendida: int

class TotaisTipoResp(BaseModel):
    quantidade: int
    valor_reais: float

class Totais30DiasResp(BaseModel):
    entradas: TotaisTipoResp
    saidas: TotaisTipoResp

class DiaGraficoResp(BaseModel):
    data: date
    entradas_qtd: int
    entradas_rs: float
    saidas_qtd: int
    saidas_rs: float

class ProdutoEstoqueResp(BaseModel):
    id: UUID
    nome: str
    qtd_estoque: int

class DashboardResponse(BaseModel):
    produto_mais_vendido: ProdutoVendaResp | None
    totais_30_dias: Totais30DiasResp
    grafico_diario: list[DiaGraficoResp]
    estoque_atual: list[ProdutoEstoqueResp]
    produtos_estoque_critico: int