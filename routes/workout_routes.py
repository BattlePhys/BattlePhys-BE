from fastapi import APIRouter, Query, Depends
from controllers.workout_controller import WorkoutController
from models.workout_models.new_workout import NewWorkout
from models.user_models.user import User
from security.authentication import Authenticate


router = APIRouter()


@router.get("/workouts", status_code=200)
async def get_all_workouts(
    user_id: str = Query(None), sort_by_date: bool = Query(True)
):
    return await WorkoutController.get_all_workouts(user_id, sort_by_date)


@router.get("/workouts/{id}", status_code=200)
async def get_workout_by_id(id: str):
    return await WorkoutController.get_by_id(id)


@router.post("/workouts", status_code=201)
async def post_workout(
    workout: NewWorkout,
    current_user: User = Depends(Authenticate.get_current_active_user),
):
    return await WorkoutController.post_workout(workout, current_user)


@router.put("/workouts/{id}", status_code=201)
async def update_workout_by_id(id: str, updated_workout: NewWorkout, current_user: User = Depends(Authenticate.get_current_active_user)):
    return await WorkoutController.update_workout(id, updated_workout, current_user)


@router.delete("/workouts/{id}", status_code=200)
async def delete_workout_by_id(
    id: str, current_user: User = Depends(Authenticate.get_current_active_user)
):
    return await WorkoutController.delete_workout(id, current_user)
