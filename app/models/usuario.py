from .mixins import TimestampMixin
from .base import Base
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text
from app.enums.cargo import Cargo

class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cargo: Mapped[str] = mapped_column(String(20), nullable=False, default=Cargo.ESTOQUISTA.value, server_default=Cargo.ESTOQUISTA.value)
    usuario: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    movimentacoes: Mapped[list["Movimentacao"]] = relationship(back_populates="usuario")
