from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.settings import settings
from src.helpers.jwt_handler import JWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = JWT.decode(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid


def get_current_user(request: Request, token: str = Depends(JWTBearer())):
    try:
        user_payload = JWT.decode(token)
        return user_payload
    except Exception as e:
        raise HTTPException(
            status_code=403, detail="Invalid token or expired token")
