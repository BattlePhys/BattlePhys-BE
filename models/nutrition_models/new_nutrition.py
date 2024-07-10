from pydantic import BaseModel


class NewNutrition(BaseModel):
    fat: int
    carbs: int
    protein: int
    body: dict