from fastapi import HTTPException, status
from features.routines.domain import Routine
from features.routines.repository import save, get_by_id
from features.routines.schemas import RoutineCreate, RoutineRead


class RoutineController:
    def __init__(self):
        ...

    def create_routine(self, data: RoutineCreate) -> RoutineRead:
        routine = Routine(
            name=data.name
        )

        saved = save(routine)

        # DOES NOT FEEL RIGHT HERE. Controller is supposed to translate app to HTTP, raises ValueError but HTTP exception is not handled
        if saved.id is None:
            raise ValueError
        
        return RoutineRead(
            name=saved.name,
            id=saved.id
        )
    
    def get_routine(self, routine_id: int) -> RoutineRead:
        try:
            routine = get_by_id(routine_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not an existing routine of id: {id}")

        assert routine.id is not None, "DB returned a routine without an ID"

        return RoutineRead(
            name=routine.name,
            id=routine.id
        )


        
    
