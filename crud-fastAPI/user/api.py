from fastapi import APIRouter,Request,status,Depends
from . models import *
from . pydantic_models import Person,Login,Token
from fastapi.responses import JSONResponse
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from passlib.context import CryptContext

app = APIRouter()
SECRET = 'your-secret-key'

manager = LoginManager(SECRET, token_url='/login/')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post('/')
async def ragistration(data:Person):
    if await Student.exists(phone=data.phone):
        return {"status":False, "message":"Phone number already exist"}
    elif await Student.exists(email=data.email):
        return {"status":False, "message":"Email number already exist"}
    else:
        user_obj = await Student.create(name = data.name,email = data.email, phone = data.phone,password = get_password_hash(data.password))
        return user_obj


@app.get('/all/')
async def all_student():
    user_obj =await Student.all()
    return user_obj


@manager.user_loader()
async def load_user(email: str):
    if await Student.exists(email = email):
            user = Student.get(email)
            return user

@app.post('/login/')
async def login(data:Login):
    email = data.email
    user = await load_user(email)

    if not user:
        raise JSONResponse({'status':False,'message':'User Not Ragistred'}, status_code=403)
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False, 'message':'Invalid password'}, status_code=403)
    access_token = manager.create_access_token(
        data = {'sub':dict({'id':jsonable_encoder(user.id)})}
    )
    new_dict = jsonable_encoder(user)
    new_dict.update({'access_token':access_token})
    return Token(access_token= access_token, token_type = 'bearer')