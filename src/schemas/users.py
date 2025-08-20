from pydantic import BaseModel, ConfigDict

class UserRequestAdd(BaseModel):
    email: str
    username: str
    password: str

class UserAdd(BaseModel): # пайдентик схема - промежуточный слой, где будет происходить конвертация пароля в хэш-значение, которое будет далее передаваться в бд
    email: str
    username: str
    hashed_password: str

class User(BaseModel):
    id: int
    email: str
    username: str

    model_config = ConfigDict(from_attributes=True)