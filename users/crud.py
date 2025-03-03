from users import CreateUser


def create_user(user_in: CreateUser):
    user = user_in.model_dump()
    return {
        'message': 'success',
        'user': user,
    }