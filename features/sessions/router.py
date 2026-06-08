from fastapi import APIRouter, HTTPException, status
from .dependencies import ServiceDep
from .schemas import SessionCreate, SessionRead, SessionUpdate


router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.post("/", response_model=SessionRead)
def create_session(
    payload: SessionCreate,
    service: ServiceDep
) -> SessionRead:
    session = payload.to_domain()
    try:
        saved = service.create_session(session=session)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return SessionRead.from_domain(saved)        


@router.get("/{session_id}", response_model=SessionRead)
def get_session(
    session_id: int,
    service: ServiceDep
) -> SessionRead:
    try:
        session = service.get_session(session_id=session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Not an existing session of id: {session_id}"
        )

    return SessionRead.from_domain(session)


@router.get("/", response_model=list[SessionRead])
def list_sessions(
    service: ServiceDep,
    routine_id: int | None = None,
    sort_by_date: bool = False,
    descending: bool = True
) -> list[SessionRead]:
    sessions = service.list_sessions(routine_id, sort_by_date, descending)
    return [SessionRead.from_domain(session) for session in sessions]


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: int,
    payload: SessionUpdate,
    service: ServiceDep
) -> SessionRead:
    session_data = payload.model_dump(exclude_unset=True)
    try:
        updated_session = service.update_session(session_id=session_id, session_data=session_data)
    except ValueError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail=f"Not an existing session of id: {session_id}"
        )

    return SessionRead.from_domain(updated_session)


@router.delete("/{session_id}", response_model=SessionRead)
def delete_session(
    session_id: int,
    service: ServiceDep
):
    try:
        deleted_session = service.delete_session(session_id=session_id)
        return SessionRead.from_domain(deleted_session)
    except ValueError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail=f"Not an existing session of id: {session_id}"
        )