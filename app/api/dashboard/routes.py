from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, obter_usuario_logado, exigir_cargos
from app.schemas.dashboard import DashboardResponse
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.movimentacao_repository import MovimentacaoRepository
from app.services.dashboard_service import DashboardService
from app.models.usuario import Usuario

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
def obter_dashboard(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_cargos(["ADMIN", "GERENTE"]))
):
    prod_repo = ProdutoRepository(db)
    mov_repo = MovimentacaoRepository(db)
    service = DashboardService(prod_repo, mov_repo)
    
    return service.gerar_dashboard()