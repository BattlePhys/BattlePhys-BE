from bson import ObjectId

nutrition_data = [
    {
        "_id": ObjectId("23fedb7a8433a888c1aca57a"),
        "date_created": "2024-04-01T01:00:00.000000",
        "body": {"chicken breast": 300, "rice": 500},
        "fat": 100,
        "protein": 100,
        "carbs": 100,
        "user_id": "75fedb7a8433a888c1aca57d",
        "total_calories": 800,
    },
    {
        "_id": ObjectId("23fedb7a8433a888c1aca57b"),
        "date_created": "2024-04-02T02:00:00.000000",
        "body": {"egg": 100, "bread": 200, "milk": 100, "protein shake": 100},
        "fat": 100,
        "protein": 100,
        "carbs": 100,
        "user_id": "75fedb7a8433a888c1aca57d",
        "total_calories": 500,
    },
    {
        "_id": ObjectId("23fedb7a8433a888c1aca57c"),
        "date_created": "2024-04-03T03:00:00.000000",
        "body": {},
        "fat": 0,
        "protein": 0,
        "carbs": 0,
        "user_id": "75fedb7a8433a888c1aca57d",
        "total_calories": 0,
    },
]
