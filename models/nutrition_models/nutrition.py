from pydantic import BaseModel
from datetime import datetime


class Nutrition(BaseModel):
    id: str
    date_created: datetime
    fat: int
    carbs: int
    protein: int
    body: dict
    user_id: str
    total_calories: int

    def __init__(self, **data):
        if data.get("_id"):
            data["id"] = str(data["_id"])
        super().__init__(**data)
