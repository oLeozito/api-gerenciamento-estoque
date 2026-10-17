from typing import TYPE_CHECKING
from .mixins import TimestampMixin
from .base import Base
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text

if TYPE_CHECKING:
    from .produto import Produto

class Fornecedor(Base, TimestampMixin):
    __tablename__ = "fornecedores"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(14), nullable=False, unique=True, index=True)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)

    produtos: Mapped[list["Produto"]] = relationship(back_populates="fornecedor")
