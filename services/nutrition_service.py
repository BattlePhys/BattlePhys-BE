from services.timestamp_service import TimestampService
from services.user_service import UserService
from repositories.nutrition_repository import NutritionRepository
from models.nutrition_models.nutrition import Nutrition
import pymongo
from fastapi import HTTPException
from bson import ObjectId


class NutritionService:
    @staticmethod
    def calculate_total_calories(nutrition_dict):
        try:
            nutrition_dict["body"] = {
                key: int(value) for key, value in nutrition_dict["body"].items()
            }
            total_calories = sum(nutrition_dict["body"].values())
            nutrition_dict["total_calories"] = total_calories
            total_calories = sum(nutrition_dict["body"].values())
            nutrition_dict["total_calories"] = total_calories
        except ValueError as e:
            raise HTTPException(
                status_code=422, detail=f"Failed to calculate total calories, {e}"
            )

    @staticmethod
    async def create_nutrition_data(nutrition_data, current_user):
        nutrition_dict = dict(nutrition_data)
        nutrition_dict["user_id"] = current_user.id
        TimestampService.apply_timestamp_to_document(nutrition_dict)
        NutritionService.calculate_total_calories(nutrition_dict)

        db_nutrition_id = await NutritionRepository.set(nutrition_dict)

        if db_nutrition_id is None:
            return None
        else:
            await UserService.map_document_to_user(
                db_nutrition_id, current_user.id, "nutrition"
            )
            return Nutrition(**{**nutrition_dict, "id": db_nutrition_id})

    @staticmethod
    async def get_nutrition_data_by_id(id):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")

        data = await NutritionRepository.get(id)
        if data is None:
            raise HTTPException(status_code=404, detail="Nutrition data not found")
        else:
            return Nutrition(**data)

    @staticmethod
    async def remove_nutrition_data(id, current_user):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")
        if id not in current_user.nutrition:
            raise HTTPException(
                status_code=401, detail="Cannot delete other users nutrition data"
            )

        deleted_data = await NutritionRepository.delete(id)

        if deleted_data is None:
            raise HTTPException(status_code=404, detail="Nutrition data not found")
        else:
            await UserService.remove_document_id_from_user(
                id, deleted_data["user_id"], "nutrition"
            )
            return Nutrition(**deleted_data)

    @staticmethod
    async def edit_nutrition_data(id, update, current_user):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")
        if id not in current_user.nutrition:
            raise HTTPException(
                status_code=401, detail="Cannot edit other users nutrition data"
            )

        update_dict = dict(update)
        NutritionService.calculate_total_calories(update_dict)

        updated_nutrition = await NutritionRepository.edit(id, update_dict)

        if updated_nutrition is None:
            raise HTTPException(status_code=404, detail="Nutrition data not found")
        else:
            return Nutrition(**updated_nutrition)

    @staticmethod
    async def get_all_nutritional_data(user_id=None, sort_by_date=True):
        if user_id:
            if not ObjectId.is_valid(user_id):
                raise HTTPException(status_code=400, detail="Invalid id")

        query = {"user_id": user_id} if user_id else {}

        nutrition_data = await NutritionRepository.get_all(query)

        if nutrition_data is None:
            raise HTTPException(status_code=404, detail="Nutrition data not found")
        else:
            sorted_nutrition_data = (
                nutrition_data.sort("date_created", pymongo.DESCENDING)
                if sort_by_date
                else nutrition_data.sort("date_created", pymongo.ASCENDING)
            )
            nutrition_list = []
            for document in sorted_nutrition_data:
                nutrition_list.append(Nutrition(**document))

            if len(nutrition_list) > 0:
                return nutrition_list
            else:
                raise HTTPException(status_code=404, detail="Nutrition data not found")
