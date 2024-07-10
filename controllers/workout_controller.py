from services.workout_service import WorkoutService


class WorkoutController:
    @staticmethod
    async def get_all_workouts(user_id=None, sort_by_date=True):
        workouts = await WorkoutService.get_all_workout_data(
            user_id, sort_by_date
        )
        return workouts

    @staticmethod
    async def get_by_id(id):
        workout = await WorkoutService.get_workout_data_by_id(id)
        return workout

    @staticmethod
    async def post_workout(workout, current_user):
        new_workout = await WorkoutService.create_workout_data(workout, current_user)
        return new_workout

    @staticmethod
    async def update_workout(id, update, current_user):
        updated_workout = await WorkoutService.edit_workout_data(id, update, current_user)
        return updated_workout

    @staticmethod
    async def delete_workout(id, current_user):
        deleted_workout = await WorkoutService.remove_workout_data(id, current_user)
        return deleted_workout
