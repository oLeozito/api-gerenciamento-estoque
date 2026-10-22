from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.produto import Produto

class ProdutoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Produto]:
        query = select(Produto)
        return list(self.session.scalars(query).all())

    def get_by_id(self, id: UUID) -> Produto | None:
        query = select(Produto).where(Produto.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_codigo(self, codigo: str) -> Produto | None:
        query = select(Produto).where(Produto.codigo == codigo)
        return self.session.execute(query).scalar_one_or_none()

    def create(self, produto: Produto) -> Produto:
        self.session.add(produto)
        self.session.commit()
        self.session.refresh(produto)
        return produto

    def update(self, produto: Produto) -> Produto:
        self.session.commit()
        self.session.refresh(produto)
        return produto

    def delete(self, produto: Produto) -> None:
        self.session.delete(produto)
        self.session.commit()