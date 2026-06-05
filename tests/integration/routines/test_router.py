import pytest
from fastapi import status 
from fastapi.testclient import TestClient
from main import create_app
from features.routines.repository import RoutineRepository
from features.routines.service import RoutineService
from features.routines.dependencies import get_routine_service


@pytest.fixture
def test_client(tmp_path):
    app = create_app()
    test_file = tmp_path / "test_repo.json"

    def override_service():
        repo = RoutineRepository(storage_file=test_file)
        return RoutineService(repo=repo)

    app.dependency_overrides[get_routine_service] = override_service

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


def test_create_routine_success(test_client, make_routine_payload):
    """
    Tests the request body against the pydantic schemas, and roundtrip data integrity.
    200 if boundary validation passes.
    """

    payload = make_routine_payload()
    
    response = test_client.post("/api/v1/routines", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert "routine_id" in body
    # validate that the response has all the high level fields of the payload. 
    assert {k: v for k, v in payload.items() if k != "exercises"}.items() <= body.items()
    assert len(body["exercises"]) == len(payload["exercises"])


def test_create_fails_domain_validation(test_client, make_routine_payload):
    """
    If the payload satisfies the DTO contract, but violates domain invariants.
    """
    payload = make_routine_payload(name="a")

    response = test_client.post("/api/v1/routines", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Routine name must be at least two characters long."


def test_create_fails_validation(test_client, make_routine_payload):
    """
    Triggers if the request body does not map with the schema.
    """

    payload = make_routine_payload(exercises=None)
    
    response = test_client.post("/api/v1/routines", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT    


def test_get_routine_by_id_success(test_client, make_routine_payload):
    """
    Returns status code 200 if the routine with the specified ID is persisted.
    """
    payload = make_routine_payload()

    post_response = test_client.post("/api/v1/routines", json=payload)
    response_id = post_response.json()["routine_id"]

    print(post_response.json())
    print(response_id)
    
    get_response = test_client.get(f"/api/v1/routines/{response_id}")
    print(get_response.json())
    assert get_response.status_code == status.HTTP_200_OK

    body = get_response.json()
    assert body["name"] == "pull day"
    assert body["routine_id"] == response_id


def test_get_all_routines_empty(test_client):
    get_response = test_client.get(f"/api/v1/routines")

    assert get_response.status_code == status.HTTP_200_OK

    body = get_response.json()
    assert body == []


