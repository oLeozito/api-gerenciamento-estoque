from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from app.repositories.usuario_repository import UsuarioRepository

class AuthService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def autenticar_usuario(self, usuario: str, senha_plana: str):
        user = self.repository.get_by_usuario(usuario)
        
        if not user or not verify_password(senha_plana, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # O payload leva o ID (sub) e o cargo (role) para validação nas rotas
        token = create_access_token(data={"sub": str(user.id), "role": user.cargo})
        return token