from fastapi import Depends, APIRouter


from users.schemas import UserSchema
from auth import utils as auth_utils

from api_v1.demo_jwt_auth.dependecies import validate_auth_user, get_current_active_auth_user
from api_v1.demo_jwt_auth.schemas import TokenInfo

router = APIRouter(prefix="/jwt", tags=["JWT"])

@router.post(
    '/login',
    response_model=TokenInfo
)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email,
        # 'logged_in': ,
    }
    access_token = auth_utils.encode_jwt(
        jwt_payload
    )
    return {
        'access_token': access_token,
        'token_type': 'Bearer',
    }


@router.get('/users/me')
def auth_user_check_self_info(
        user: UserSchema = Depends(get_current_active_auth_user)
):
    return {
        'username': user.username,
        'email': user.email,
    }