from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.movimentacao import Movimentacao

class MovimentacaoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Movimentacao]:
        query = select(Movimentacao).order_by(Movimentacao.data.desc())
        return list(self.session.scalars(query).all())

    def get_by_id(self, id: UUID) -> Movimentacao | None:
        query = select(Movimentacao).where(Movimentacao.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_produto_id(self, produto_id: UUID) -> list[Movimentacao]:
        query = select(Movimentacao).where(Movimentacao.produto_id == produto_id).order_by(Movimentacao.data.desc())
        return list(self.session.scalars(query).all())