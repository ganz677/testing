from fastapi import APIRouter, Depends
from users import CreateUser
from users import crud


router = APIRouter(prefix="/users", tags=["users"])





@router.get("/")
async def get_users():
    pass

@router.get("/{user_id}")
async def get_user(user_id: int):
    pass

@router.post("/create/")
async def create_user(user: CreateUser):
    return crud.create_user(user_in=user)

@router.patch("/{user_id}")
async def update_user():
    pass

@router.delete("/{user_id}")
async def delete_user():
    pass