from fastapi import HTTPException, status
from features.routines.domain import Routine
from features.routines.repository import RoutineRepository
from features.routines.schemas import RoutineCreate, RoutineRead, RoutineUpdate


class RoutineController:
    def __init__(self, repo: RoutineRepository):
        self.repo = repo
        

    def create_routine(self, payload: RoutineCreate) -> RoutineRead:
        routine = payload.to_domain()
        saved = self.repo.save_routine(routine)
        return RoutineRead.from_domain(saved)
    
    
    def get_routine(self, routine_id: int) -> RoutineRead:
        try:
            routine = self.repo.get_routine_by_id(routine_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not an existing routine of id: {routine_id}")

        return RoutineRead.from_domain(routine)


    def list_routines_controller(self) -> list[RoutineRead]:
        routines = self.repo.list_routines()
        
        return [RoutineRead.from_domain(routine) for routine in routines]


    def update_routine(self, routine_id: int, payload: RoutineUpdate) -> RoutineRead:
        try:
            routine = self.repo.get_routine_by_id(routine_id)
        except ValueError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Not an existing routine of id: {routine_id}")
        
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(routine, key, value)
        
        self.repo.update_routine(routine)

        return RoutineRead.from_domain(routine)
    

    def delete_routine(self, routine_id: int) -> RoutineRead:
        try:
            return RoutineRead.from_domain(self.repo.remove_routine(routine_id))
        except ValueError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Not an existing routine of id: {routine_id}")