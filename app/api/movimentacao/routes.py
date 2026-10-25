from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse
from app.services.movimentacao_service import MovimentacaoService
from app.repositories.movimentacao_repository import MovimentacaoRepository
from app.repositories.produto_repository import ProdutoRepository
from app.api.deps import obter_usuario_logado
from app.core.database import get_db
from app.models.usuario import Usuario
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])

@router.get("", response_model=list[MovimentacaoResponse], status_code=status.HTTP_200_OK)
def listar_movimentacoes(
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    tipo: Optional[str] = None,
    fornecedor_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    repository = MovimentacaoRepository(db)
    service = MovimentacaoService(repository, None)
    return service.listar_todas(data_inicio, data_fim, tipo, fornecedor_id)

@router.get("/produto/{produto_id}", response_model=list[MovimentacaoResponse], status_code=status.HTTP_200_OK)
def listar_movimentacoes_por_produto(
    produto_id: UUID,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    repository = MovimentacaoRepository(db)
    service = MovimentacaoService(repository, None)
    return service.buscar_por_produto(produto_id)

@router.post("", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_movimentacao(
    mov_in: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado) 
):
    mov_repo = MovimentacaoRepository(db)
    prod_repo = ProdutoRepository(db)
    service = MovimentacaoService(mov_repo, prod_repo)
    
    return service.criar_movimentacao(mov_in, usuario_id=usuario_atual.id)