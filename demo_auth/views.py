import secrets
import time
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix="/demo_auth", tags=["Demo Authentication"])

security = HTTPBasic()



@router.get('/basic-auth/')
def demo_basic_credentials(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        'message': 'complete',
        'username': credentials.username,
        'password': credentials.password,
    }



# basic

usernames_to_passwords = {
    'admin': 'admin',
    'john': 'qwerty',
}

def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
        headers={'WWW-Authenticate': 'Basic'},
    )
    correct_password = usernames_to_passwords[credentials.username]
    if correct_password is None:
        raise unauthed_exc
    # secrets
    if not secrets.compare_digest(
        credentials.password.encode('utf8'),
        correct_password.encode('utf8'),
    ):
        raise unauthed_exc
    return credentials.username

@router.get('/basic-auth-username/')
def demo_basic_credentials_username(
        auth_username: str = Depends(get_auth_user_username),
):
    return {
        'message': f'hi! {auth_username}',
        'username': auth_username,
    }




#headers

static_auth_token_to_username = {
    '573225192e86d45a90fa95c6e87079': 'admin',
    '535330d9d1cf02fac5660814b5ae33' : 'john'
}

def get_username_by_static_auth_token(
    static_token: str = Header(alias='X-Static-Auth-Token')
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid static auth token',
        )


@router.get('/some-http-header-auth/')
def demo_auth_some_http_header(
        username: Annotated[str, Depends(get_username_by_static_auth_token)],
):
    return {
        'message': f'hi! {username}',
        'username': username,
    }


#cookie

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY: str = 'web-app-session-id'

def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post('/login_cookie/')
def demo_auth_login_set_cookie(
        response: Response,
        username: Annotated[str, Depends(get_username_by_static_auth_token)],
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time.time()),
    }
    response.set_cookie(
        COOKIE_SESSION_ID_KEY,
        session_id,
    )
    return {
        'result': 'ok'
    }

def get_session_data(
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid session id',
        )
    return COOKIES[session_id]

@router.get('/check_cookie/')
def demo_auth_check_cookie(
        user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data['username']
    return {
        'message': f'hello {username}',
        **user_session_data,
    }

@router.get('/logout_cookie/')
def demo_logout_cookie(
        response: Response,
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
        user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id, None)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data['username']
    return {
        'message': f'Bye {username}',
    }
