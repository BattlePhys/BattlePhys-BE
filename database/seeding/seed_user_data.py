from bson import ObjectId

user_data = [
    {
        "_id": ObjectId("65fedb7a8433a888c1aca57c"),
        "username": "user1",
        "full_name": "test name 1",
        "email": "user1@email.com",
        "hashed_password": "$2b$12$u7qTSdNfDzvFtAscVCmXH.cji.RiPbU5CVxJl1Eb.zzUAGG5USegW",
        "workouts": [],
        "nutrition": [],
        "friends": ["75fedb7a8433a888c1aca57d", "95fedb7a8433a888c1aca57f"],
        "disabled": False,
    },
    {
        "_id": ObjectId("75fedb7a8433a888c1aca57d"),
        "username": "user2",
        "full_name": "test name 2",
        "email": "user2@email.com",
        "hashed_password": "$2b$12$u7qTSdNfDzvFtAscVCmXH.cji.RiPbU5CVxJl1Eb.zzUAGG5USegX",
        "workouts": ["65fedb7a8433a888c1aca57a", "65fedb7a8433a888c1aca57b"],
        "nutrition": [],
        "friends": ["65fedb7a8433a888c1aca57c", "95fedb7a8433a888c1aca57f"],
        "disabled": False,
    },
    {
        "_id": ObjectId("85fedb7a8433a888c1aca57e"),
        "username": "user3",
        "full_name": "test name 3",
        "email": "user3@email.com",
        "hashed_password": "$2c$12$u7qTSdNfDzvFtAscVCmXH.cji.RiPbU5CVxJl1Eb.zzUAGG5USegY",
        "workouts": ["65fedb7a8433a888c1aca57c"],
        "nutrition": [],
        "friends": [],
        "disabled": False,
    },
    {
        "_id": ObjectId("95fedb7a8433a888c1aca57f"),
        "username": "user4",
        "full_name": "test name 4",
        "email": "user4@email.com",
        "hashed_password": "$2c$12$u7qTSdNfDzvFtAscVCmXH.cji.RiPbU5CVxJl1Eb.zzUAGG5USegZ",
        "workouts": [],
        "nutrition": [],
        "friends": ["65fedb7a8433a888c1aca57c", "75fedb7a8433a888c1aca57d"],
        "disabled": False,
    },
]
    
