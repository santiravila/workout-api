from typing import Annotated
from fastapi import APIRouter, Depends
from features.sessions.schemas import SessionCreate, SessionRead
from features.sessions.controller import SessionController
from features.sessions.repository import SessionRepository

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])

def get_session_controller() -> SessionController:
    repo = SessionRepository()
    return SessionController(repo)


ControllerDep = Annotated[SessionController, Depends(get_session_controller)]


@router.post("/")
def create_session(
    payload: SessionCreate,
    controller: ControllerDep
) -> SessionRead:
    return controller.create_session(payload=payload)
