from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from app.models.produto import Produto

from app.models.movimentacao import Movimentacao

class MovimentacaoRepository:
    def __init__(self, session: Session):
        self.session = session

    def pesquisar_avancado(
        self, 
        data_inicio: datetime | None, 
        data_fim: datetime | None,
        tipo: str | None,
        fornecedor_id: UUID | None
    ) -> list[Movimentacao]:
        
        query = select(Movimentacao)

        # Se o fornecedor foi passado, fazemos o JOIN dinâmico com Produto
        if fornecedor_id:
            query = query.join(Produto).where(Produto.fornecedor_id == fornecedor_id)
            
        if data_inicio:
            query = query.where(Movimentacao.data >= data_inicio)
        if data_fim:
            query = query.where(Movimentacao.data <= data_fim)
        if tipo:
            query = query.where(Movimentacao.tipo == tipo)

        # Ordena sempre da mais recente para a mais antiga
        query = query.order_by(Movimentacao.data.desc())
        
        return list(self.session.scalars(query).all())

    def get_by_id(self, id: UUID) -> Movimentacao | None:
        query = select(Movimentacao).where(Movimentacao.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_produto_id(self, produto_id: UUID) -> list[Movimentacao]:
        query = select(Movimentacao).where(Movimentacao.produto_id == produto_id).order_by(Movimentacao.data.desc())
        return list(self.session.scalars(query).all())