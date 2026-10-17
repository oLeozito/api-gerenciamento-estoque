from typing import TYPE_CHECKING
from .mixins import TimestampMixin
from .base import Base
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, text

if TYPE_CHECKING:
    from .categoria import Categoria
    from .fornecedor import Fornecedor
    from .movimentacao import Movimentacao

class Produto(Base,TimestampMixin):
    __tablename__ = "produtos"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(String(600), nullable=True)
    preco_custo: Mapped[float] = mapped_column(nullable=False)
    preco_venda: Mapped[float] = mapped_column(nullable=False)
    qtd_estoque: Mapped[int] = mapped_column(nullable=False) 
    categoria_id: Mapped[UUID] = mapped_column(ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False, index=True)
    fornecedor_id: Mapped[UUID] = mapped_column(ForeignKey("fornecedores.id", ondelete="RESTRICT"), nullable=False, index=True)

    categoria: Mapped["Categoria"] = relationship(back_populates="produtos")
    fornecedor: Mapped["Fornecedor"] = relationship(back_populates="produtos")
    movimentacoes: Mapped[list["Movimentacao"]] = relationship(back_populates="produto")
    # peso
