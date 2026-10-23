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

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])

@router.get("", response_model=list[MovimentacaoResponse], status_code=status.HTTP_200_OK)
def listar_movimentacoes(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    repository = MovimentacaoRepository(db)
    # Passamos None para o produto_repo pois não precisamos dele no GET genérico
    service = MovimentacaoService(repository, None) 
    return service.listar_todas()

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
    # Estoquista tem passe livre aqui
    usuario_atual: Usuario = Depends(obter_usuario_logado) 
):
    # Instanciamos os dois repositórios dividindo a MESMA sessão de banco
    mov_repo = MovimentacaoRepository(db)
    prod_repo = ProdutoRepository(db)
    service = MovimentacaoService(mov_repo, prod_repo)
    
    return service.criar_movimentacao(mov_in)