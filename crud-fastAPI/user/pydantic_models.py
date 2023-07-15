from pydantic import BaseModel


class Person(BaseModel):
    name :str
    email : str
    phone :int
    password :str


class Login(BaseModel):
    email :str
    password :str

class Token(BaseModel):
    access_token:str
    token_type:str = 'bearer'