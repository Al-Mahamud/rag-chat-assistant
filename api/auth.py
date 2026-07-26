import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME

security = HTTPBasic()


def require_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    valid_user = secrets.compare_digest(credentials.username, BASIC_AUTH_USERNAME)
    valid_pass = secrets.compare_digest(credentials.password, BASIC_AUTH_PASSWORD)
    if not (valid_user and valid_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
