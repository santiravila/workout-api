from typing import Annotated
from fastapi import APIRouter, Depends
from features.sessions.schemas import SessionCreate, SessionRead, SessionUpdate
from features.sessions.controller import SessionController
from features.sessions.repository import SessionRepository


router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


def get_session_controller() -> SessionController:
    repo = SessionRepository()
    return SessionController(repo)


ControllerDep = Annotated[SessionController, Depends(get_session_controller)]


@router.post("/", response_model=SessionRead)
def create_session(
    payload: SessionCreate,
    controller: ControllerDep
) -> SessionRead:
    return controller.create_session(payload=payload)


@router.get("/{session_id}", response_model=SessionRead)
def get_session(
    session_id: int,
    controller: ControllerDep
) -> SessionRead:
    return controller.get_session(session_id)


@router.get("/", response_model=list[SessionRead])
def list_sessions(
    controller: ControllerDep
) -> list[SessionRead]:
    return controller.list_sessions_controller()


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: int,
    payload: SessionUpdate,
    controller: ControllerDep
) -> SessionRead:
    return controller.update_session(session_id, payload)


@router.delete("/{session_id}", response_model=SessionRead)
def delete_session(
    session_id: int,
    controller: ControllerDep
):
    return controller.delete_session(session_id)