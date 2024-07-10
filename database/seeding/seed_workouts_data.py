from bson import ObjectId

workouts_data = [
    {
        "_id": ObjectId("65fedb7a8433a888c1aca57a"),
        "type": "individual",
        "title": "title 1",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "user_id": "75fedb7a8433a888c1aca57d",
        "date_created": "2024-04-05T18:00:00.000000",
        "notes": "note 1",
    },
    {
        "_id": ObjectId("65fedb7a8433a888c1aca57b"),
        "type": "individual",
        "title": "title 2",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "user_id": "75fedb7a8433a888c1aca25a",
        "date_created": "2024-04-05T19:00:00.000000",
        "notes": "note 2",
    },
    {
        "_id": ObjectId("65fedb7a8433a888c1aca57c"),
        "type": "battlephys",
        "title": "title 3",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "user_id": "85fedb7a8433a888c1aca57e",
        "date_created": "2024-04-05T20:00:00.000000",
        "notes": "note 3",
    },
]
