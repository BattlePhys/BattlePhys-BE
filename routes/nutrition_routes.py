from fastapi import APIRouter, Query, Depends
from controllers.nutrition_controller import NutritionController
from models.nutrition_models.new_nutrition import NewNutrition
from models.user_models.user import User
from security.authentication import Authenticate

router = APIRouter()


@router.get("/nutrition", status_code=200)
async def get_all(user_id: str = Query(None), sort_by_date: bool = Query(True)):
    return await NutritionController.get_all(user_id, sort_by_date)


@router.get("/nutrition/{id}", status_code=200)
async def get_by_id(id: str):
    return await NutritionController.get_by_id(id)


@router.post("/nutrition", status_code=201)
async def post_nutrition(
    nutrition: NewNutrition,
    current_user: User = Depends(Authenticate.get_current_active_user),
):
    return await NutritionController.post_nutrition(nutrition, current_user)


@router.put("/nutrition/{id}", status_code=200)
async def update_nutrition(
    id: str,
    update: NewNutrition,
    current_user: User = Depends(Authenticate.get_current_active_user),
):
    return await NutritionController.update_nutrition(id, update, current_user)


@router.delete("/nutrition/{id}", status_code=200)
async def delete_nutrition(
    id: str, current_user: User = Depends(Authenticate.get_current_active_user)
):
    return await NutritionController.delete_nutrition(id, current_user)
