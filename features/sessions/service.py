from .repository import SessionRepository
from features.routines.repository import RoutineRepository
from .domain import Session, Exercise


class SessionService:
    def __init__(self, session_repo: SessionRepository, routine_repo: RoutineRepository):
        self.session_repo = session_repo
        self.routine_repo = routine_repo
        
    def create_session(self, session: Session) -> Session:
        self.routine_repo.get_routine_by_id(session.routine_id)        
        saved = self.session_repo.save_session(session)
        return saved

    
    def get_session(self, session_id: int) -> Session:
        return self.session_repo.get_session_by_id(session_id=session_id)
    
     
    def list_sessions(self, routine_id: int | None = None, sort_by_date: bool = False, descending: bool = True) -> list[Session]:
        return self.session_repo.list_sessions(routine_id, sort_by_date, descending)


    def update_session(self, session_id: int, session_data: dict) -> Session:
        session = self.session_repo.get_session_by_id(session_id)
                
        for key, value in session_data.items():
            if key == "exercises":
                session.exercises = [
                    Exercise.from_dict(ex) for ex in value
                ]
            else:
                setattr(session, key, value)
        
        updated_session = self.session_repo.update_session(session)

        return updated_session
    
    
    def delete_session(self, session_id: int) -> Session:
        return self.session_repo.remove_session(session_id)
        