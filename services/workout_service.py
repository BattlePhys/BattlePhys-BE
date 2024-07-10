from services.timestamp_service import TimestampService
from services.user_service import UserService
from repositories.workout_repository import WorkoutRepository
from models.workout_models.workout import Workout
import pymongo
from fastapi import HTTPException
from bson import ObjectId


class WorkoutService:
    @staticmethod
    async def create_workout_data(workout_data, current_user):
        workout_dict = dict(workout_data)
        workout_dict["user_id"] = current_user.id
        TimestampService.apply_timestamp_to_document(workout_dict)

        db_workout_id = await WorkoutRepository.set(workout_dict)

        if db_workout_id is None:
            return None
        else:
            await UserService.map_document_to_user(
                db_workout_id, current_user.id, "workouts"
            )
            return Workout(**{**workout_dict, "id": db_workout_id})

    @staticmethod
    async def get_workout_data_by_id(id):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")

        data = await WorkoutRepository.get(id)
        if data is None:
            raise HTTPException(status_code=404, detail="Workout data not found")
        else:
            return Workout(**data)

    @staticmethod
    async def remove_workout_data(id, current_user):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")
        if id not in current_user.workouts:
            raise HTTPException(
                status_code=401, detail="Cannot delete other users workout data"
            )

        deleted_data = await WorkoutRepository.delete(id)

        if deleted_data is None:
            raise HTTPException(status_code=404, detail="Workout data not found")
        else:
            await UserService.remove_document_id_from_user(
                id, deleted_data["user_id"], "workouts"
            )
            return Workout(**deleted_data)

    @staticmethod
    async def edit_workout_data(id, update, current_user):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid id")
        if id not in current_user.workouts:
            raise HTTPException(
                status_code=401, detail="Cannot edit other users workout data"
            )

        update_dict = dict(update)

        updated_workout = await WorkoutRepository.edit(id, update_dict)

        if updated_workout is None:
            raise HTTPException(status_code=404, detail="Workout data not found")
        else:
            return Workout(**updated_workout)

    @staticmethod
    async def get_all_workout_data(user_id=None, sort_by_date=True):
        if user_id:
            if not ObjectId.is_valid(user_id):
                raise HTTPException(status_code=400, detail="Invalid id")

        query = {"user_id": user_id} if user_id else {}

        workout_data = await WorkoutRepository.get_all(query)

        if workout_data is None:
            raise HTTPException(status_code=404, detail="Workout data not found")
        else:
            sorted_workout_data = (
                workout_data.sort("date_created", pymongo.DESCENDING)
                if sort_by_date
                else workout_data.sort("date_created", pymongo.ASCENDING)
            )
            workout_list = []
            for document in sorted_workout_data:
                workout_list.append(Workout(**document))

            if len(workout_list) > 0:
                return workout_list
            else:
                raise HTTPException(status_code=404, detail="Workout data not found")
