import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import create_app
from features.routines.repository import RoutineRepository
from features.routines.controller import RoutineController
from features.routines.router import get_routine_controller


@pytest.fixture
def test_client(tmp_path):
    app = create_app()
    test_file = tmp_path / "test_repo.json"

    def override_controller():
        repo = RoutineRepository(storage_file=test_file)
        return RoutineController(repo=repo)

    app.dependency_overrides[get_routine_controller] = override_controller

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


# eventually inject payload from a fixture factory
def test_create_routine_success(test_client):
    """
    Tests the request body against the pydantic schemas, and roundtrip data integrity.
    200 if boundary validation passes.
    """

    payload = {
        "name": "pull day",
        "exercises":[
            {
                "name": "pullups",
                "reps_per_set":[10, 10, 10]
            }
        ]
    }
    
    response = test_client.post("/api/v1/routines", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert "routine_id" in body
    # validate that the response has all the high level fields of the payload. 
    assert {k: v for k, v in payload.items() if k != "exercises"}.items() <= body.items()
    assert len(body["exercises"]) == len(payload["exercises"])


def test_create_fails_domain_validation(test_client):
    """
    If the payload satisfies the DTO contract, but violates domain invariants.
    """
    payload = {
        "name": "a",
        "exercises":[
            {
                "name": "pullups",
                "reps_per_set":[10, 10, 10]
            }
        ]
    }
    
    response = test_client.post("/api/v1/routines", json=payload)
    print(response.json())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Routine name must be at least two characters long."


def test_create_fails_validation(test_client):
    """
    Triggers if the request body does not map with the schema.
    """

    payload = {
        "name": "a"
    }
    
    response = test_client.post("/api/v1/routines", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT    


def test_get_routine_by_id_success(test_client):
    """
    Returns status code 200 if the routine with the specified ID is persisted.
    """
    payload = {
        "name": "pull day",
        "exercises":[
            {
                "name": "pullups",
                "reps_per_set":[10, 10, 10]
            }
        ]
    }

    post_response = test_client.post("/api/v1/routines", json=payload)
    response_id = post_response.json()["routine_id"]

    get_response = test_client.get(f"/api/v1/routines/{response_id}")

    assert get_response.status_code == status.HTTP_200_OK

    body = get_response.json()
    assert body["name"] == "pull day"
    assert body["routine_id"] == response_id


def test_get_all_routines_empty(test_client):
    get_response = test_client.get(f"/api/v1/routines")

    assert get_response.status_code == status.HTTP_200_OK

    body = get_response.json()
    assert body == []


