import pytest
from database.connection import MongoConnection
from database.seeding.seed_user_data import user_data
from database.seeding.seed_workouts_data import workouts_data
from database.seeding.seed_nutrition_data import nutrition_data
from database.seeding.authorised_user_data.seed_authorised_data import (
    create_authorised_workout_data,
    create_authorised_nutrition_data,
)
from main import app
from fastapi.testclient import TestClient
from bson import ObjectId

test_db = MongoConnection()


@pytest.fixture(scope="function")
def clean_db():
    test_db.drop_collection("users")
    test_db.drop_collection("workouts")
    test_db.drop_collection("nutrition")

    test_db.seed_collection("users", user_data)
    test_db.seed_collection("workouts", workouts_data)
    test_db.seed_collection("nutrition", nutrition_data)

    yield test_db


@pytest.fixture(scope="function")
def empty_db():
    test_db.drop_collection("users")
    test_db.drop_collection("workouts")
    test_db.drop_collection("nutrition")

    yield test_db


@pytest.fixture(scope="function")
def client():
    test_client = TestClient(app)
    return test_client


@pytest.fixture(scope="function")
def authorised_test_client(client):
    user_to_post = {
        "username": "test user",
        "email": "test_user@email.com",
        "password": "test password",
        "full_name": "test user",
    }

    response = client.post("/api/users", json=user_to_post)
    authorised_user = response.json()

    login_data = {"username": "test user", "password": "test password"}
    login_response = client.post("/token", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {access_token}"})

    return client, authorised_user


@pytest.fixture(scope="function")
def authorised_data(authorised_test_client):
    _, user = authorised_test_client

    workout_data = create_authorised_workout_data(user["id"])
    nutrition_data = create_authorised_nutrition_data(user["id"])

    test_db.seed_collection("nutrition", nutrition_data)
    test_db.seed_collection("workouts", workout_data)

    user_collection = test_db.get_collection("users")
    user["workouts"].append("83fedb6a8433a888c1aca37d")
    user["nutrition"].append("81fedb6a8433a888c1aca37e")

    user_collection.find_one_and_update(
        {"_id": ObjectId(user["id"])}, {"$set": user}, return_document=True
    )
