from database.connection import workout_collection
from bson import ObjectId



class WorkoutRepository:
    @staticmethod
    async def get_all(query):
        try:
            return workout_collection.find(query)
        except Exception as e:
            print(f"Error getting workout data: {e}")
            return None

    @staticmethod
    async def get(id):
        try:
            return workout_collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error getting workout data: {e}")
            return None

    @staticmethod
    async def edit(id, update):
        try:
            return workout_collection.find_one_and_update(
                {"_id": ObjectId(id)}, {"$set": update}, return_document=True
            )
        except Exception as e:
            print(f"Error updating workout data: {e}")
        return None

    @staticmethod
    async def delete(id):
        try:
            return workout_collection.find_one_and_delete({"_id": ObjectId(id)})
        except Exception as e:
            print(f"Error deleting workout data: {e}")
            return None

    @staticmethod
    async def set(workout_dict):
        try:
            db_workout = workout_collection.insert_one(workout_dict)
            return db_workout.inserted_id
        except Exception as e:
            print(f"An exception occurred when saving workout: {e}")
            return None
