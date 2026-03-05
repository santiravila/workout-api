from fastapi import HTTPException, status
from features.routines.domain import Routine
from features.routines.repository import RoutineRepository
from features.routines.schemas import RoutineCreate, RoutineRead, RoutineUpdate

repo = RoutineRepository()

class RoutineController:
    def __init__(self):
        ...

    def create_routine(self, data: RoutineCreate) -> RoutineRead:
        routine = Routine(
            name=data.name
        )

        saved = repo.save(routine)

        return RoutineRead.from_domain(saved)
    
    
    def get_routine(self, routine_id: int) -> RoutineRead:
        try:
            routine = repo.get_by_id(routine_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not an existing routine of id: {routine_id}")

        return RoutineRead.from_domain(routine)



    def list_routines_controller(self) -> list[RoutineRead]:
        routines = repo.list_routines()
        
        return [RoutineRead.from_domain(routine) for routine in routines]


    def update_routine(self, routine_id: int, payload: RoutineUpdate) -> RoutineRead:
        try:
            routine = repo.get_by_id(routine_id)
        except ValueError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Not an existing routine of id: {routine_id}")
        
        update_data = payload.model_dump(exclude_unset=True)
        for key_name in update_data:
            setattr(routine, key_name, update_data[key_name])
        return RoutineRead.from_domain(routine)