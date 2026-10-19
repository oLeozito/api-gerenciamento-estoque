from fastapi import FastAPI
from app.api.auth.routes import router as auth_router

app = FastAPI(title="愚公移山 Variedades API")

app.include_router(auth_router)
