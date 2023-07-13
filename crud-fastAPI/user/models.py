from tortoise.models import Model
from tortoise import Tortoise,fields

class User(Model):
    id = fields.IntField()
    name = fields.CharField(255)
    email = fields.CharField(255, unique=True)
    mobile = fields.IntField(10)
    password = fields.CharField(255)


class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255)
    email = fields.CharField(255, unique=True)
    phone = fields.IntField(pk=False)
    password = fields.CharField(255)


Tortoise.init_models(['user.models'],'models')