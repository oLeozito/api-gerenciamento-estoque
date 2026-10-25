from typing import TYPE_CHECKING
from datetime import datetime
from .mixins import TimestampMixin
from .base import Base
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, text
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from .produto import Produto

class Movimentacao(Base, TimestampMixin):
    __tablename__ = "movimentacoes"
    __table_args__ = (
        CheckConstraint("quantidade > 0", name="ck_movimentacoes_quantidade_positiva"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    usuario_id: Mapped[UUID] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    quantidade: Mapped[int] = mapped_column(nullable=False)
    valor_unitario: Mapped[float] = mapped_column(nullable=True)
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # RESTRICT preserva o historico: um produto com movimentacoes nao pode ser apagado fisicamente.
    produto_id: Mapped[UUID] = mapped_column(ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False, index=True)

    produto: Mapped["Produto"] = relationship(back_populates="movimentacoes")
    usuario: Mapped["Usuario"] = relationship(back_populates="movimentacoes")