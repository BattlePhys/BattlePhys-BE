from bson import ObjectId


def create_authorised_workout_data(user_id):
    return (
        {
            "_id": ObjectId("83fedb6a8433a888c1aca37d"),
            "type": "individual",
            "title": "title 1",
            "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
            "notes": "note 4",
            "user_id": user_id,
            "date_created": "2024-04-01T18:00:00.000000",
        },
    )


def create_authorised_nutrition_data(user_id):
    return (
        {
            "_id": ObjectId("81fedb6a8433a888c1aca37e"),
            "date_created": "2024-04-01T18:00:00.000000",
            "fat": 1,
            "carbs": 2,
            "protein": 3,
            "body": {"foo": 1, "bar": 2},
            "user_id": user_id,
            "total_calories": 6,
        },
    )
