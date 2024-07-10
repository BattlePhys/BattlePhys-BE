from bson import ObjectId
from database.connection import nutrition_collection


class NutritionRepository:
    @staticmethod
    async def get_all(query):
        try:
            return nutrition_collection.find(query)
        except Exception as e:
            print(f"Error getting nutrition data: {e}")
            return None

    @staticmethod
    async def get(id):
        try:
            return nutrition_collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error getting nutrition data: {e}")
            return None

    @staticmethod
    async def edit(id, update):
        try:
            return nutrition_collection.find_one_and_update(
                {"_id": ObjectId(id)}, {"$set": update}, return_document=True
            )
        except Exception as e:
            print(f"Error updating nutrition data: {e}")
        return None

    @staticmethod
    async def delete(id):
        try:
            return nutrition_collection.find_one_and_delete({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error deleting nutrition data: {e}")
            return None

    @staticmethod
    async def set(nutrition_dict):
        try:
            db_nutrition = nutrition_collection.insert_one(nutrition_dict)
            return db_nutrition.inserted_id
        except Exception as e:
            print(f"An exception occurred when saving nutrition: {e}")
            return None
