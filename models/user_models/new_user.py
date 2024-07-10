from pydantic import BaseModel, EmailStr


class NewUser(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
