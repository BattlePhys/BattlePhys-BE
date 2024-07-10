from bson import ObjectId

# CREATE


def test_post_workout_201(clean_db, authorised_test_client):
    client, user = authorised_test_client
    user_id = user["id"]
    workout_to_post = {
        "type": "individual",
        "title": "test post workout",
        "body": {"exercise 1": "10", "exercise 2": "20", "exercise 3": "30"},
        "notes": "test note",
    }
    response = client.post("/api/workouts", json=workout_to_post)
    response_data = response.json()

    assert response.status_code == 201
    assert len(response_data) == 7
    assert "id" in response_data
    assert isinstance(response_data["id"], str)
    assert ObjectId.is_valid(response_data["id"])
    assert "date_created" in response_data
    assert isinstance(response_data["date_created"], str)
    assert response_data["type"] == "individual"
    assert response_data["title"] == "test post workout"
    assert response_data["body"] == {
        "exercise 1": "10",
        "exercise 2": "20",
        "exercise 3": "30",
    }
    assert response_data["user_id"] == user_id
    assert response_data["notes"] == "test note"

    user_to_check = client.get(f"/api/users/{user_id}")
    user_data = user_to_check.json()

    assert response_data["id"] in user_data["workouts"]


def test_post_workout_422_missing_property(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    workout_to_post = {
        "type": "individual",
        "body": {"exercise 1": "10", "exercise 2": "20", "exercise 3": "30"},
        "notes": "test note",
    }
    response = client.post("/api/workouts", json=workout_to_post)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "missing"
    assert response_data["detail"][0]["loc"] == ["body", "title"]
    assert response_data["detail"][0]["msg"] == "Field required"


def test_post_workout_422_invalid_property(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    workout_to_post = {
        "type": "banana",
        "title": "test incorrect type",
        "body": {"exercise 1": "10", "exercise 2": "20", "exercise 3": "30"},
        "notes": "test note",
    }
    response = client.post("/api/workouts", json=workout_to_post)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "value_error"
    assert response_data["detail"][0]["loc"] == ["body", "type"]
    assert (
        response_data["detail"][0]["msg"]
        == "Value error, type must be one of ('individual', 'battlephys')"
    )


def test_post_workout_422_invalid_data_type(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    workout_to_post = {
        "type": "battlephys",
        "title": 12345,
        "body": {"exercise 1": "10", "exercise 2": "20", "exercise 3": "30"},
        "notes": "test note",
    }
    response = client.post("/api/workouts", json=workout_to_post)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "string_type"
    assert response_data["detail"][0]["loc"] == ["body", "title"]
    assert response_data["detail"][0]["msg"] == "Input should be a valid string"


# READ


def test_get_all_workouts_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts")
    response_data = response.json()

    assert response.status_code == 200

    assert response_data[0]["date_created"] == "2024-04-05T20:00:00"
    assert response_data[1]["date_created"] == "2024-04-05T19:00:00"
    assert response_data[2]["date_created"] == "2024-04-05T18:00:00"

    for workout in response_data:
        assert len(workout) == 7
        assert "id" in workout
        assert isinstance(workout["id"], str)
        assert ObjectId.is_valid(workout["id"])
        assert "type" in workout
        assert isinstance(workout["type"], str)
        assert "title" in workout
        assert isinstance(workout["title"], str)
        assert "body" in workout
        assert isinstance(workout["body"], dict)
        assert "user_id" in workout
        assert isinstance(workout["user_id"], str)
        assert ObjectId.is_valid(workout["user_id"])
        assert "date_created" in workout
        assert isinstance(workout["date_created"], str)
        assert isinstance(workout["notes"], str)
        assert "notes" in workout


def test_get_all_workouts_404(empty_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {"detail": "Workout data not found"}


def test_get_all_workouts_with_user_id_query_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts?user_id=75fedb7a8433a888c1aca57d")
    response_data = response.json()

    assert response.status_code == 200
    for workout in response_data:
        assert len(workout) == 7
        assert "id" in workout
        assert isinstance(workout["id"], str)
        assert ObjectId.is_valid(workout["id"])
        assert "type" in workout
        assert isinstance(workout["type"], str)
        assert "title" in workout
        assert isinstance(workout["title"], str)
        assert "body" in workout
        assert isinstance(workout["body"], dict)
        assert "user_id" in workout
        assert isinstance(workout["user_id"], str)
        assert ObjectId.is_valid(workout["user_id"])
        assert "date_created" in workout
        assert isinstance(workout["date_created"], str)
        assert isinstance(workout["notes"], str)
        assert "notes" in workout


def test_get_all_workouts_with_user_id_query_404(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts?user_id=65fedb7a8433a888c1aca57c")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {"detail": "Workout data not found"}


def test_get_all_workouts_with_user_id_query_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts?user_id=banana")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}


def test_get_workouts_sort_by_ascending_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts?sort_by_date=False")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data[0]["date_created"] == "2024-04-05T18:00:00"
    assert response_data[1]["date_created"] == "2024-04-05T19:00:00"
    assert response_data[2]["date_created"] == "2024-04-05T20:00:00"


def test_get_workout_by_id_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts/65fedb7a8433a888c1aca57a")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": "65fedb7a8433a888c1aca57a",
        "type": "individual",
        "title": "title 1",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "user_id": "75fedb7a8433a888c1aca57d",
        "date_created": "2024-04-05T18:00:00",
        "notes": "note 1",
    }


def test_get_workout_by_id_404(empty_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts/65fedb7a8433a888c1aca57a")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {"detail": "Workout data not found"}


def test_get_workout_by_id_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.get("/api/workouts/banana")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}


# UPDATE


def test_update_workout_201(clean_db, authorised_test_client, authorised_data):
    client, user = authorised_test_client
    user_id = user["id"]

    updated_workout = {
        "type": "battlephys",
        "title": "title 4",
        "body": {"exercise 1": "10", "exercise 2": "10", "new exercise": "10"},
        "notes": "note 1",
    }
    response = client.put("api/workouts/83fedb6a8433a888c1aca37d", json=updated_workout)
    response_data = response.json()

    assert response.status_code == 201
    assert response_data == {
        "id": "83fedb6a8433a888c1aca37d",
        "type": "battlephys",
        "title": "title 4",
        "body": {"exercise 1": "10", "exercise 2": "10", "new exercise": "10"},
        "notes": "note 1",
        "user_id": user_id,
        "date_created": "2024-04-01T18:00:00",
    }


def test_update_workout_additional_properties_201(
    clean_db, authorised_test_client, authorised_data
):
    client, user = authorised_test_client
    user_id = user["id"]

    updated_workout = {
        "type": "individual",
        "title": "title 4",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "notes": "note 1",
        "foo": "bar",
    }
    response = client.put("api/workouts/83fedb6a8433a888c1aca37d", json=updated_workout)
    response_data = response.json()

    assert response.status_code == 201
    assert response_data == {
        "id": "83fedb6a8433a888c1aca37d",
        "type": "individual",
        "title": "title 4",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "notes": "note 1",
        "user_id": user_id,
        "date_created": "2024-04-01T18:00:00",
    }


def test_update_workout_401(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    updated_workout = {
        "type": "battlephys",
        "title": "title 4",
        "body": {"exercise 1": "10", "exercise 2": "10", "new exercise": "10"},
        "notes": "note 1",
    }
    response = client.put("api/workouts/83fedb6a8433a888c1aca37d", json=updated_workout)
    response_data = response.json()

    assert response.status_code == 401
    assert response_data == {"detail": "Cannot edit other users workout data"}


# def test_update_workout_404(clean_db, authorised_test_client):
#     client, _ = authorised_test_client

#     updated_workout = {
#         "type": "individual",
#         "title": "title 4",
#         "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
#         "user_id": "85fedb7a8433a888c1aca57e",
#     }
#     response = client.put("api/workouts/47fedb7a8433a888c1aca57c", json=updated_workout)
#     response_data = response.json()

#     assert response.status_code == 404
#     assert response_data == {"detail": "Workout not found"}


def test_update_workout_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    updated_workout = {
        "type": "individual",
        "title": "title 4",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "notes": "note 1",
    }
    response = client.put("api/workouts/banana", json=updated_workout)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}


def test_update_workout_422_missing_property(
    clean_db, authorised_test_client, authorised_data
):
    client, _ = authorised_test_client

    updated_workout = {
        "type": "individual",
        "title": "title 4",
        "notes": "note 1",
    }
    response = client.put("api/workouts/83fedb6a8433a888c1aca37d", json=updated_workout)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "missing"
    assert response_data["detail"][0]["loc"] == ["body", "body"]
    assert response_data["detail"][0]["msg"] == "Field required"


def test_update_workout_422_invalid_property(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    updated_workout = {
        "type": "individual",
        "title": "title 4",
        "body": "foo",
        "notes": "note 1",
    }
    response = client.put("api/workouts/83fedb6a8433a888c1aca37d", json=updated_workout)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "dict_type"
    assert response_data["detail"][0]["loc"] == ["body", "body"]
    assert response_data["detail"][0]["msg"] == "Input should be a valid dictionary"


# # # DELETE


def test_delete_workout_200(clean_db, authorised_test_client, authorised_data):
    client, user = authorised_test_client
    user_id = user["id"]

    response = client.delete("api/workouts/83fedb6a8433a888c1aca37d")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": "83fedb6a8433a888c1aca37d",
        "type": "individual",
        "title": "title 1",
        "body": {"exercise 1": "10", "exercise 2": "10", "exercise 3": "10"},
        "notes": "note 4",
        "user_id": user_id,
        "date_created": "2024-04-01T18:00:00",
    }

    user = client.get(f"/api/users/{user_id}")
    user_data = user.json()

    assert response_data["id"] not in user_data["workouts"]


def test_delete_workout_401(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.delete("api/workouts/83fedb6a8433a888c1aca37d")
    response_data = response.json()

    assert response.status_code == 401
    assert response_data == {"detail": "Cannot delete other users workout data"}


# def test_delete_workout_404(clean_db):
#     client, _ = authorised_test_client

#     response = client.delete("api/workouts/13fedb7a8433a888c1aca57c")
#     response_data = response.json()

#     assert response.status_code == 404
#     assert response_data == {"detail": "Workout not found"}


def test_delete_workout_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client

    response = client.delete("api/workouts/banana")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}
