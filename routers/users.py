from fastapi import APIRouter
from pydantic import BaseModel
from user_jwt import createToken

login_user = APIRouter()



class User(BaseModel):
    email: str
    password: str


@login_user.post('/login', tags=['authentication'])
def login(user: User):
    if user.email == 'string' and user.password == 'string':
        token: str = createToken(user.model_dump())
    print(token)
    return user
