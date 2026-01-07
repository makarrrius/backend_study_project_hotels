from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserRequestLogin(BaseModel):
    email: EmailStr
    password: str


class UserAdd(
    BaseModel
):  # пайдентик схема - промежуточный слой, где будет происходить конвертация пароля в хэш-значение, которое будет далее передаваться в бд
    email: EmailStr
    username: str
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr
    username: str


class UserWithHashedPassword(User):
    hashed_password: str
