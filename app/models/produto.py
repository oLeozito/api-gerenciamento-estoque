from .mixins import TimestampMixin
from .base import Base
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text

class Produto(Base,TimestampMixin):
    __tablename__ = "produtos"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(String(600), nullable=True)
    preco_custo: Mapped[float] = mapped_column(nullable=False)
    preco_venda: Mapped[float] = mapped_column(nullable=False)
    qtd_estoque: Mapped[int] = mapped_column(nullable=False) 
    categoria: Mapped[str] = mapped_column(String(150), nullable=False)    
    # peso

    # TODO: Colocar os relationships