from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from server.shared.config import settings
from server.shared.exceptions import InvalidActionError

_ALGORITHM = "HS256"
_ACCESS_TYPE = "access"
_REFRESH_TYPE = "refresh"


def _make_token(user_id: UUID, token_type: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": str(user_id), "type": token_type, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=_ALGORITHM)


def create_access_token(user_id: UUID) -> str:
    return _make_token(
        user_id,
        _ACCESS_TYPE,
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(user_id: UUID) -> str:
    return _make_token(
        user_id,
        _REFRESH_TYPE,
        timedelta(days=settings.refresh_token_expire_days),
    )


def decode_access_token(token: str) -> UUID:
    return _decode(token, expected_type=_ACCESS_TYPE)


def decode_refresh_token(token: str) -> UUID:
    return _decode(token, expected_type=_REFRESH_TYPE)


def _decode(token: str, expected_type: str) -> UUID:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[_ALGORITHM])
    except JWTError:
        raise InvalidActionError("Token inválido ou expirado.")

    if payload.get("type") != expected_type:
        raise InvalidActionError(f"Tipo de token incorreto. Esperado: {expected_type}.")

    sub = payload.get("sub")
    if not sub:
        raise InvalidActionError("Token sem subject.")

    return UUID(sub)
