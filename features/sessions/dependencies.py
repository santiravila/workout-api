from fastapi import Depends
from typing import Annotated
from .service import SessionService
from .repository import SessionRepository
from features.routines.repository import RoutineRepository


def get_session_service() -> SessionService:
    session_repo = SessionRepository()
    routine_repo = RoutineRepository()
    return SessionService(session_repo=session_repo, routine_repo=routine_repo)


ServiceDep = Annotated[
    SessionService,
    Depends(get_session_service)
]