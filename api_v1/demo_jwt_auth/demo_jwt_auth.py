from fastapi import (
    Depends,
    APIRouter
)
from fastapi.security import HTTPBearer

from users.schemas import UserSchema
from api_v1.demo_jwt_auth.helpers import (
    create_access_token,
    create_refresh_token
)

from api_v1.demo_jwt_auth.dependecies import (
    validate_auth_user,
    get_current_active_auth_user,
    get_current_token_payload
)
from api_v1.demo_jwt_auth.schemas import TokenInfo

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])


# Здесь создается jwt
@router.post(
    '/login/',
    response_model=TokenInfo
)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get('/users/me')
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat
    }