from pydantic import BaseModel
from datetime import datetime


class Workout(BaseModel):
    id: str
    type: str
    title: str
    body: dict
    notes: str
    user_id: str
    date_created: datetime

    def __init__(self, **data):
        if data.get("_id"):
            data["id"] = str(data["_id"])
        super().__init__(**data)
