from features.routines.repository import RoutineRepository
from .domain import Routine


class RoutineService:
    def __init__(self, repo: RoutineRepository):
        self.repo = repo
        
    def create_routine(self, routine: Routine) -> Routine:
        saved = self.repo.save_routine(routine)
        return saved
    
    
    def get_routine(self, routine_id: int) -> Routine:
        routine = self.repo.get_routine_by_id(routine_id)
        return routine


    def list_routines(self) -> list[Routine]:
        routines = self.repo.list_routines()
        return routines


    def update_routine(self, routine_id: int, update_data: dict) -> Routine:    
        routine = self.repo.get_routine_by_id(routine_id=routine_id) 

        for key, value in update_data.items():
            setattr(routine, key, value)

        updated_routine = self.repo.update_routine(routine)        
        
        return updated_routine
    

    def delete_routine(self, routine_id: int) -> Routine:
        removed_routine = self.repo.remove_routine(routine_id) 
        
        return removed_routine