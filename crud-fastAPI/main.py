from fastapi import FastAPI
from user import api as UserAPI
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware


Middleware = [
    Middleware(SessionMiddleware,secret_key = 'super-secret')
]

app = FastAPI(middleware=Middleware)
app.include_router(UserAPI.app)



register_tortoise(
    app,
    db_url="postgres://postgres:sharma@127.0.0.1/test1",
    modules={'models': ['user.models',]},
    generate_schemas=True,
    add_exception_handlers=True
)