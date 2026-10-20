from fastapi import FastAPI
from app.api.auth.routes import router as auth_router
from app.api.categoria.routes import router as categoria_router

app = FastAPI(title="愚公移山 Variedades API")

app.include_router(auth_router)
app.include_router(categoria_router)