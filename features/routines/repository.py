from features.routines.domain import Routine
import json
from pathlib import Path

# __file__ is the absolute path to repository.py
# .parent goes up one level to the /routines/ folder
CURRENT_DIR = Path(__file__).parent 

DATA_DIR = CURRENT_DIR / "data"
STORAGE_FILE = DATA_DIR / "routines.json"


class RoutineRepository:
    def __init__(self, storage_file=None):
        self.storage_file = STORAGE_FILE if storage_file is None else storage_file 


    def _load(self) -> list[Routine]:
        loaded_routines = []

        # Ensure the data directory exists
        DATA_DIR.mkdir(exist_ok=True)
        
        if not self.storage_file.exists(): return []
        
        with open(self.storage_file, mode="r") as infile:
            try:
                data = json.load(infile)
            except json.JSONDecodeError:
                return []
            
            for routine in data["routines"]:
                loaded_routine = Routine.from_dict(routine)
                loaded_routines.append(loaded_routine)

            return loaded_routines
                

    def _save(self, routines: list[Routine]):
        data = {
            "routines": [routine.to_dict() for routine in routines]
        }

        with open(self.storage_file, "w") as outfile:
            json.dump(data, outfile, indent=2)


    def save_routine(self, routine: Routine) -> Routine:
        routines = self._load()
        greatest_id = max([r.id for r in routines if r.id is not None], default=0)
        
        routine.id = greatest_id + 1
        routines.append(routine)
        self._save(routines)

        return routine


    def get_routine_by_id(self, routine_id: int) -> Routine:
        routines = self._load()
        for routine in routines:
            if routine.id == routine_id:
                return routine
        
        raise ValueError(f"Not found")


    def list_routines(self) -> list[Routine]:
        return self._load()


    def update_routine(self, updated_routine: Routine) -> Routine:
        routines = self._load()

        for index, routine in enumerate(routines):
            if routine.id == updated_routine.id:
                routines[index] = updated_routine
                self._save(routines)
                return updated_routine
        
        raise ValueError("Not found")
    

    def remove_routine(self, routine_id: int) -> Routine:
        routines = self._load()
        for index, routine in enumerate(routines):
            if routine.id == routine_id:
                deleted_routine = routines.pop(index)
                self._save(routines)
                return deleted_routine
        
        raise ValueError(f"Not found")
    
