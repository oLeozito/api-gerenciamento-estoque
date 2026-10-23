from fastapi import FastAPI
from app.api.auth.routes import router as auth_router
from app.api.categoria.routes import router as categoria_router
from app.api.fornecedor.routes import router as fornecedor_router
from app.api.produto.routes import router as produto_router
from app.api.movimentacao.routes import router as movimentacao_router

app = FastAPI(title="愚公移山 Variedades API")

app.include_router(auth_router)
app.include_router(categoria_router)
app.include_router(fornecedor_router)
app.include_router(produto_router)
app.include_router(movimentacao_router)