from services.nutrition_service import NutritionService


class NutritionController:
    @staticmethod
    async def get_all(user_id=None, sort_by_date=True):
        response = await NutritionService.get_all_nutritional_data(
            user_id, sort_by_date
        )
        return response

    @staticmethod
    async def get_by_id(id):
        response = await NutritionService.get_nutrition_data_by_id(id)
        return response

    @staticmethod
    async def post_nutrition(nutrition, current_user):
        response = await NutritionService.create_nutrition_data(nutrition, current_user)
        return response

    @staticmethod
    async def update_nutrition(id, update, current_user):
        response = await NutritionService.edit_nutrition_data(id, update, current_user)
        return response

    @staticmethod
    async def delete_nutrition(id, current_user):
        response = await NutritionService.remove_nutrition_data(id, current_user)
        return response
