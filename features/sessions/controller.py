from fastapi import HTTPException, status
from features.sessions.repository import SessionRepository
from features.sessions.schemas import SessionCreate, SessionRead, SessionUpdate


class SessionController:
    def __init__(self, repo: SessionRepository):
        self.repo = repo
        
    def create_session(self, payload: SessionCreate) -> SessionRead:
        session = payload.to_domain()
        saved = self.repo.save_session(session)

        return SessionRead.from_domain(saved)

    
    def get_session(self, session_id: int) -> SessionRead:
        try:
            session = self.repo.get_session_by_id(session_id=session_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Not an existing session of id: {session_id}"
            )

        return SessionRead.from_domain(session)

     
    def list_sessions_controller(self) -> list[SessionRead]:
        sessions = self.repo.list_sessions()
        
        return [SessionRead.from_domain(session) for session in sessions]


    def update_session(self, session_id: int, payload: SessionUpdate) -> SessionRead:
        try:
            session = self.repo.get_session_by_id(session_id)
        except ValueError:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail=f"Not an existing session of id: {session_id}"
            )
        
        update_data = payload.model_dump(exclude_unset=True)
        
        session.apply_patch(update_data)
        self.repo.update_session(session)

        return SessionRead.from_domain(session)
    
    def delete_session(self, session_id: int) -> SessionRead:
        try:
            return SessionRead.from_domain(self.repo.remove_session(session_id))
        except ValueError:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail=f"Not an existing session of id: {session_id}"
            )