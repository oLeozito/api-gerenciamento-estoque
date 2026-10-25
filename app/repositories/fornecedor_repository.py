from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.fornecedor import Fornecedor

class FornecedorRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Fornecedor]:
        query = select(Fornecedor)
        return list(self.session.scalars(query).all())

    def get_by_id(self, id: UUID) -> Fornecedor | None:
        query = select(Fornecedor).where(Fornecedor.id == id)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_cnpj(self, cnpj: str) -> Fornecedor | None:
        query = select(Fornecedor).where(Fornecedor.cnpj == cnpj)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_email(self, email: str) -> Fornecedor | None:
        query = select(Fornecedor).where(Fornecedor.email == email)
        return self.session.execute(query).scalar_one_or_none()

    def create(self, fornecedor: Fornecedor) -> Fornecedor:
        self.session.add(fornecedor)
        self.session.commit()
        self.session.refresh(fornecedor)
        return fornecedor

    def update(self, fornecedor: Fornecedor) -> Fornecedor:
        self.session.commit()
        self.session.refresh(fornecedor)
        return fornecedor

    def delete(self, fornecedor: Fornecedor) -> None:
        self.session.delete(fornecedor)
        self.session.commit()