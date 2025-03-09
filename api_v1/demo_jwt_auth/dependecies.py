from jwt.exceptions import InvalidTokenError

from fastapi import (
    Form,
    HTTPException,
    status,
    Depends
)
from fastapi.security import (
    OAuth2PasswordBearer,
    # HTTPBearer,
    # HTTPAuthorizationCredentials

)

from api_v1.demo_jwt_auth.crud import users_db
from auth import utils as auth_utils
from users.schemas import UserSchema

from api_v1.demo_jwt_auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exception

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password
    ):
        raise unauthed_exception

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not active")

    return user


# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login/",
)


def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token error: {e}'
        )
    return payload

def validate_token_type(
        payload: dict,
        token_type: str
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Token type must be {token_type!r}, now token type is {current_token_type!r}'
    )

def get_user_by_token_sub(
        payload: dict
) -> UserSchema:
    username: str | None = payload.get('sub')
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'token invalid: user not found'
    )

def get_current_user_by_token_of_type(
        token_type: str,
):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)
    return get_auth_user_from_token

get_current_auth_user = get_current_user_by_token_of_type(token_type=ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_current_user_by_token_of_type(token_type=REFRESH_TOKEN_TYPE)

def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )

