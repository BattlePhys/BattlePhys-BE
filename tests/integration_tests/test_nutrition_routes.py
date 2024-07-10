from main import app
from fastapi.testclient import TestClient
from bson import ObjectId


client = TestClient(app)

# CREATE


def test_post_nutrition_200(clean_db, authorised_test_client):
    client, user = authorised_test_client
    user_id = user["id"]
    data_to_post = {
        "fat": 1,
        "carbs": 2,
        "protein": 3,
        "body": {"food 1": 10, "food 2": 20},
    }
    response = client.post("/api/nutrition", json=data_to_post)
    response_data = response.json()

    assert response.status_code == 201
    assert len(response_data) == 8
    assert "id" in response_data
    assert isinstance(response_data["id"], str)
    assert ObjectId.is_valid(response_data["id"])
    assert "date_created" in response_data
    assert isinstance(response_data["date_created"], str)
    assert response_data["fat"] == 1
    assert response_data["carbs"] == 2
    assert response_data["protein"] == 3
    assert response_data["body"] == {"food 1": 10, "food 2": 20}
    assert response_data["user_id"] == user_id
    assert response_data["total_calories"] == 30

    user_to_check = client.get(f"/api/users/{user_id}")
    user_data = user_to_check.json()

    assert response_data["id"] in user_data["nutrition"]


def test_post_nutrition_with_casting_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    data_to_post = {
        "fat": "1",
        "carbs": "2",
        "protein": "3",
        "body": {"food 1": 10, "food 2": 20},
    }
    response = client.post("/api/nutrition", json=data_to_post)
    response_data = response.json()

    assert response.status_code == 201
    assert len(response_data) == 8
    assert response_data["fat"] == 1
    assert response_data["carbs"] == 2
    assert response_data["protein"] == 3


def test_post_nutrition_422_missing_property(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    data_to_post = {
        "carbs": 2,
        "protein": 3,
        "body": {"food 1": 10, "food 2": 20},
    }
    response = client.post("/api/nutrition", json=data_to_post)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "missing"
    assert response_data["detail"][0]["loc"] == ["body", "fat"]
    assert response_data["detail"][0]["msg"] == "Field required"


def test_post_nutrition_422_invalid_data_type(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    data_to_post = {
        "fat": "banana",
        "carbs": 2,
        "protein": 3,
        "body": {"food 1": 10, "food 2": 20},
    }
    response = client.post("/api/nutrition", json=data_to_post)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "int_parsing"
    assert response_data["detail"][0]["loc"] == ["body", "fat"]
    assert (
        response_data["detail"][0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )


def test_post_nutrition_422_invalid_body_values(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    data_to_post = {
        "fat": "1",
        "carbs": 2,
        "protein": 3,
        "body": {"food 1": "banana", "food 2": 20},
    }
    response = client.post("/api/nutrition", json=data_to_post)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data == {
        "detail": "Failed to calculate total calories, invalid literal for int() with base 10: 'banana'"
    }


def test_post_nutrition_401_unauthorised_user_id(clean_db, client):
    data_to_post = {
        "fat": 1,
        "carbs": 2,
        "protein": 3,
        "body": {"food 1": 10, "food 2": 20},
    }
    response = client.post("/api/nutrition", json=data_to_post)
    response_data = response.json()

    assert response.status_code == 401
    assert response_data == {"detail": "Not authenticated"}


# READ


def test_get_all_nutrition_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition")
    response_data = response.json()

    assert response.status_code == 200
    for response in response_data:
        assert len(response) == 8
        assert "id" in response
        assert isinstance(response["id"], str)
        assert ObjectId.is_valid(response["id"])
        assert "date_created" in response
        assert isinstance(response["date_created"], str)
        assert "fat" in response
        assert isinstance(response["fat"], int)
        assert "carbs" in response
        assert isinstance(response["carbs"], int)
        assert "protein" in response
        assert isinstance(response["protein"], int)
        assert "total_calories" in response
        assert isinstance(response["total_calories"], int)
        assert "body" in response
        assert isinstance(response["body"], dict)
        assert "user_id" in response
        assert isinstance(response["user_id"], str)
        assert ObjectId.is_valid(response["user_id"])


def test_get_all_nutrition_by_user_id_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition?user_id=75fedb7a8433a888c1aca57d")
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 3
    assert response_data[0]["date_created"] == "2024-04-03T03:00:00"
    assert response_data[1]["date_created"] == "2024-04-02T02:00:00"
    assert response_data[2]["date_created"] == "2024-04-01T01:00:00"
    for response in response_data:
        assert len(response) == 8
        assert "id" in response
        assert isinstance(response["id"], str)
        assert ObjectId.is_valid(response["id"])
        assert "date_created" in response
        assert isinstance(response["date_created"], str)
        assert "fat" in response
        assert isinstance(response["fat"], int)
        assert "carbs" in response
        assert isinstance(response["carbs"], int)
        assert "protein" in response
        assert isinstance(response["protein"], int)
        assert "total_calories" in response
        assert isinstance(response["total_calories"], int)
        assert "body" in response
        assert isinstance(response["body"], dict)
        assert "user_id" in response
        assert isinstance(response["user_id"], str)
        assert ObjectId.is_valid(response["user_id"])


def test_get_all_nutrition_by_user_id_ascending_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get(
        "/api/nutrition?user_id=75fedb7a8433a888c1aca57d&sort_by_date=False"
    )
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 3
    assert response_data[0]["date_created"] == "2024-04-01T01:00:00"
    assert response_data[1]["date_created"] == "2024-04-02T02:00:00"
    assert response_data[2]["date_created"] == "2024-04-03T03:00:00"


def test_get_all_nutrition_404(empty_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {"detail": "Nutrition data not found"}


def test_get_all_nutrition_by_user_id_404(empty_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition?user_id=75fedb7a8433a888c1aca57d")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {"detail": "Nutrition data not found"}


def test_get_all_nutrition_by_user_id_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition?user_id=banana")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}


def test_get_nutrition_by_id_200(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition/23fedb7a8433a888c1aca57a")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": "23fedb7a8433a888c1aca57a",
        "date_created": "2024-04-01T01:00:00",
        "body": {"chicken breast": 300, "rice": 500},
        "fat": 100,
        "protein": 100,
        "carbs": 100,
        "user_id": "75fedb7a8433a888c1aca57d",
        "total_calories": 800,
    }


def test_get_nutrition_by_id_404(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition/23fedb7a8433a888c1aca57f")
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {"detail": "Nutrition data not found"}


def test_get_nutrition_by_id_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.get("/api/nutrition/banana")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}


# UPDATE


def test_update_nutrition_200(clean_db, authorised_test_client, authorised_data):
    client, user = authorised_test_client
    user_id = user["id"]
    updated_nutrition = {
        "body": {"chicken breast": 301, "rice": 501},
        "fat": 101,
        "protein": 102,
        "carbs": 103,
    }

    response = client.put(
        "/api/nutrition/81fedb6a8433a888c1aca37e", json=updated_nutrition
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": "81fedb6a8433a888c1aca37e",
        "date_created": "2024-04-01T18:00:00",
        "fat": 101,
        "carbs": 103,
        "protein": 102,
        "body": {"chicken breast": 301, "rice": 501},
        "user_id": user_id,
        "total_calories": 802,
    }


def test_update_nutrition_extra_fields_200(
    clean_db, authorised_test_client, authorised_data
):
    client, user = authorised_test_client
    user_id = user["id"]
    updated_nutrition = {
        "body": {"chicken breast": 301, "rice": 501},
        "fat": 101,
        "protein": 102,
        "carbs": 103,
        "foo": "bar",
    }

    response = client.put(
        "/api/nutrition/81fedb6a8433a888c1aca37e", json=updated_nutrition
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": "81fedb6a8433a888c1aca37e",
        "date_created": "2024-04-01T18:00:00",
        "fat": 101,
        "carbs": 103,
        "protein": 102,
        "body": {"chicken breast": 301, "rice": 501},
        "user_id": user_id,
        "total_calories": 802,
    }


def test_update_nutrition_casting_200(
    clean_db, authorised_test_client, authorised_data
):
    client, user = authorised_test_client
    user_id = user["id"]
    updated_nutrition = {
        "body": {"chicken breast": 301, "rice": 501},
        "fat": "101",
        "protein": "102",
        "carbs": "103",
    }

    response = client.put(
        "/api/nutrition/81fedb6a8433a888c1aca37e", json=updated_nutrition
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": "81fedb6a8433a888c1aca37e",
        "date_created": "2024-04-01T18:00:00",
        "fat": 101,
        "carbs": 103,
        "protein": 102,
        "body": {"chicken breast": 301, "rice": 501},
        "user_id": user_id,
        "total_calories": 802,
    }


# def test_update_nutrition_404(clean_db):
#     updated_nutrition = {
#         "body": {"chicken breast": 301, "rice": 501},
#         "fat": 101,
#         "protein": 102,
#         "carbs": 103,
#         "user_id": "75fedb7a8433a888c1aca57d",
#     }

#     response = client.put(
#         "/api/nutrition/89fedb7a8433a888c1aca35b", json=updated_nutrition
#     )
#     response_data = response.json()

#     assert response.status_code == 404
#     assert response_data == {"detail": "Nutrition data not found"}


def test_update_nutrition_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    updated_nutrition = {
        "body": {"chicken breast": 301, "rice": 501},
        "fat": 101,
        "protein": 102,
        "carbs": 103,
    }

    response = client.put("/api/nutrition/banana", json=updated_nutrition)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}


# def test_update_nutrition_422_invalid_user_id(clean_db, authorised_test_client):
#     client, _ = authorised_test_client
#     updated_nutrition = {
#         "body": {"chicken breast": 301, "rice": 501},
#         "fat": 101,
#         "protein": 102,
#         "carbs": 103,
#     }

#     response = client.put(
#         "/api/nutrition/23fedb7a8433a888c1aca57a", json=updated_nutrition
#     )
#     response_data = response.json()

#     assert response.status_code == 422
#     assert response_data["detail"][0]["type"] == "value_error"
#     assert response_data["detail"][0]["loc"] == ["body", "user_id"]
#     assert (
#         response_data["detail"][0]["msg"]
#         == "Value error, user_id must be a valid MongoDB ObjectId"
#     )


def test_update_nutrition_422_missing_prperty(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    updated_nutrition = {
        "fat": 101,
        "protein": 102,
        "carbs": 103,
    }

    response = client.put(
        "/api/nutrition/23fedb7a8433a888c1aca57a", json=updated_nutrition
    )
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "missing"
    assert response_data["detail"][0]["loc"] == ["body", "body"]
    assert response_data["detail"][0]["msg"] == "Field required"


def test_update_nutrition_422_invalid_data_type(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    updated_nutrition = {
        "body": {"chicken breast": 301, "rice": 501},
        "fat": 101,
        "protein": "banana",
        "carbs": 103,
    }

    response = client.put(
        "/api/nutrition/81fedb6a8433a888c1aca37e", json=updated_nutrition
    )
    response_data = response.json()

    assert response.status_code == 422
    assert response_data["detail"][0]["type"] == "int_parsing"
    assert response_data["detail"][0]["loc"] == ["body", "protein"]
    assert (
        response_data["detail"][0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )


def test_update_nutrition_400_invalid_body_values(
    clean_db, authorised_test_client, authorised_data
):
    client, _ = authorised_test_client
    updated_nutrition = {
        "body": {"chicken breast": "banana", "rice": 501},
        "fat": 101,
        "protein": 102,
        "carbs": 103,
    }

    response = client.put(
        "/api/nutrition/81fedb6a8433a888c1aca37e", json=updated_nutrition
    )
    response_data = response.json()

    assert response.status_code == 422
    assert response_data == {
        "detail": "Failed to calculate total calories, invalid literal for int() with base 10: 'banana'"
    }


# # DELETE


def test_delete_nutrition_200(clean_db, authorised_test_client, authorised_data):
    client, user = authorised_test_client
    user_id = user["id"]
    response = client.delete("/api/nutrition/81fedb6a8433a888c1aca37e")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {
        "id": "81fedb6a8433a888c1aca37e",
        "date_created": "2024-04-01T18:00:00",
        "fat": 1,
        "carbs": 2,
        "protein": 3,
        "body": {"foo": 1, "bar": 2},
        "user_id": user_id,
        "total_calories": 6,
    }

    user = client.get(f"/api/users/{user_id}")
    user_data = user.json()

    assert response_data["id"] not in user_data["workouts"]


# def test_delete_nutrition_404(clean_db):
#     response = client.delete("/api/nutrition/62fedb7a8433a888c1aca95b")
#     response_data = response.json()

#     assert response.status_code == 404
#     assert response_data == {"detail": "Nutrition data not found"}


def test_delete_nutrition_400(clean_db, authorised_test_client):
    client, _ = authorised_test_client
    response = client.delete("/api/nutrition/banana")
    response_data = response.json()

    assert response.status_code == 400
    assert response_data == {"detail": "Invalid id"}
