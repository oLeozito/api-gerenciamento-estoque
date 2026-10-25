from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.categoria import Categoria

class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Categoria]:
        query = select(Categoria)
        return list(self.session.scalars(query).all())

    def get_by_id(self, id: UUID) -> Categoria | None:
        query = select(Categoria).where(Categoria.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_nome(self, nome: str) -> Categoria | None:
        query = select(Categoria).where(Categoria.nome == nome)
        return self.session.execute(query).scalar_one_or_none()

    def create(self, categoria: Categoria) -> Categoria:
        self.session.add(categoria)
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def update(self, categoria: Categoria) -> Categoria:
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def delete(self, categoria: Categoria) -> None:
        self.session.delete(categoria)
        self.session.commit()