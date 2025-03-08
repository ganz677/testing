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

from auth import utils as auth_utils
from users.schemas import UserSchema

john = UserSchema(
    username="john",
    password=auth_utils.hash_password(
        'qwerty'
    ),
    email='john@example.com',
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password(
        'secret'
    )
)

users_db: dict[str, UserSchema] = {
        john.username: john,
        sam.username: sam,
}


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
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    # token = credentials.credentials
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


def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload)
) -> UserSchema:
    username: str | None = payload.get('sub')
    if user := users_db.get(username):
        return user
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)"
        )



def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )

