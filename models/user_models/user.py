from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    email: EmailStr
    workouts: list
    nutrition: list
    friends: list
    username: str
    full_name: str
    disabled: bool
    hashed_password: str
    
    
    def __init__(self, **data):
        if data.get('_id'):
            data['id'] = str(data['_id'])
        super().__init__(**data)