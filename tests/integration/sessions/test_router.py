from main import create_app
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from features.sessions.repository import SessionRepository
from features.routines.repository import RoutineRepository
from features.sessions.controller import SessionController
from features.routines.service import RoutineService
from features.sessions.router import get_session_controller
from features.routines.dependencies import get_routine_service 


# send requests to the API through a test client using temporary repository files
@pytest.fixture
def test_client(tmp_path):
    app = create_app() # clean Dependency Graph per testing function
    sessions_test_file = tmp_path / "test_sessions.json"
    routines_test_file = tmp_path / "test_routines.json"

    def override_session_controller():
        session_repo = SessionRepository(storage_file=sessions_test_file)
        routine_repo = RoutineRepository(storage_file=routines_test_file)
        return SessionController(session_repo, routine_repo)

    def override_routine_service():
        repo = RoutineRepository(storage_file=routines_test_file)
        return RoutineService(repo=repo)

    app.dependency_overrides[get_session_controller] = override_session_controller
    app.dependency_overrides[get_routine_service] = override_routine_service

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()    


# create a valid session (maps to the SessionCreate DTO and does not violate domain invariants)
def test_create_valid_session(test_client, make_routine_payload, make_session_payload):
    valid_routine = make_routine_payload()
    
    routine_response = test_client.post("/api/v1/routines", json=valid_routine)
    routine_id = routine_response.json()["routine_id"]
    assert routine_response.status_code == status.HTTP_200_OK

    payload = make_session_payload(routine_id=routine_id)

    response = test_client.post("/api/v1/sessions", json=payload)
    assert response.status_code == status.HTTP_200_OK


# try creating a session with a ID without a corresponding persisted routine: 404 not found
def test_create_session_invalid_id(test_client, make_session_payload):
    payload = make_session_payload()

    response = test_client.post("/api/v1/sessions", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# try creating a session with a ludicrous name "1" (fails at domain validation, catched by exception handler): 400 bad request
def test_create_session_invalid_name(test_client, make_routine_payload, make_session_payload):
    valid_routine = make_routine_payload()
    routine_response = test_client.post("/api/v1/routines", json=valid_routine)
    routine_id = routine_response.json()["routine_id"]
    assert routine_response.status_code == status.HTTP_200_OK

    payload = make_session_payload(routine_name="a", routine_id=routine_id)
    response = test_client.post("/api/v1/sessions", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# try creating a session without a required field (fails at boundary): 422 unprocessable entity
def test_create_session_invalid_structure(test_client, make_session_payload):
    payload = make_session_payload(routine_name=None)

    response = test_client.post("/api/v1/sessions", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# try getting a session by id (success)
def test_get_session_by_id(test_client, make_routine_payload, make_session_payload):
    valid_routine = make_routine_payload()    
    routine_response = test_client.post("/api/v1/routines", json=valid_routine)
    routine_id = routine_response.json()["routine_id"]
    assert routine_response.status_code == status.HTTP_200_OK

    payload = make_session_payload(routine_id=routine_id)

    response_post = test_client.post("/api/v1/sessions", json=payload)
    session_id = response_post.json()["session_id"]
    assert response_post.status_code == status.HTTP_200_OK
    
    response_get = test_client.get(f"/api/v1/sessions/{session_id}")
    assert response_get.status_code == status.HTTP_200_OK


# try getting all sessions (success)
def test_get_all_sessions_empty(test_client):
    response = test_client.get("/api/v1/sessions")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body == []
