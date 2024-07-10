from pydantic import BaseModel, EmailStr


class EditableUser(BaseModel):
    email: EmailStr
    username: str
    full_name: str
