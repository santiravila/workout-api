import json
from pathlib import Path
from features.sessions.domain import Session


CURRENT_DIR = Path(__file__).parent # which directory I'm I at?

DATA_DIR = CURRENT_DIR / "data" # point to the directory im at /data
STORAGE_FILE = DATA_DIR / "sessions.json" # the storage file is at current_directory/data/sessions.json


class SessionRepository:
    def __init__(self, storage_file=None):
        self.storage_file = STORAGE_FILE if storage_file is None else storage_file 


    def _load(self) -> list[Session]:
        loaded_sessions = []

        DATA_DIR.mkdir(exist_ok=True) # data directory created
        
        if not self.storage_file.exists(): return [] 
        
        with open(self.storage_file, mode="r") as infile:
            try:
                data = json.load(infile)
            except json.JSONDecodeError:
                return []
            
            for session in data["sessions"]:
                loaded_session = Session.from_dict(session)
                loaded_sessions.append(loaded_session)

            return loaded_sessions
                

    def _save(self, sessions: list[Session]) -> None:
        data = {
            "sessions": [session.to_dict() for session in sessions]
        }

        with open(self.storage_file, "w") as outfile:
            json.dump(data, outfile, indent=2)


    def save_session(self, session: Session) -> Session:
        sessions = self._load()
        greatest_id = max([s.session_id for s in sessions if s.session_id is not None], default=0)

        session.session_id = greatest_id + 1
        sessions.append(session)
        self._save(sessions)

        return session


    def get_session_by_id(self, session_id: int) -> Session:
        sessions = self._load()
        for session in sessions:
            if session.session_id == session_id:
                return session
        
        raise ValueError(f"Not found")


    def list_sessions(self, routine_id: int | None = None, sort_by_date: bool = False, descending: bool = True) -> list[Session]:
        sessions = self._load()
        
        # Filtering
        if routine_id:
            return [session for session in sessions if session.routine_id == routine_id]

        # Sorting
        if sort_by_date:
            return sorted(sessions, key=lambda s: s.date, reverse=descending)

        return self._load()


    def update_session(self, updated_session: Session) -> Session:
        sessions = self._load()

        for index, session in enumerate(sessions):
            if session.session_id == updated_session.session_id:
                sessions[index] = updated_session
                self._save(sessions)
                return updated_session
            
        raise ValueError("Not found")
    

    def remove_session(self, session_id: int) -> Session:
        sessions = self._load()
        for index, session in enumerate(sessions):
            if session.session_id == session_id:
                deleted_session = sessions.pop(index)
                self._save(sessions)
                return deleted_session
        
        raise ValueError(f"Not found")
    
