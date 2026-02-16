#from fastapi import HTTPException, status
from features.routines.domain import Routine
from features.routines.repository import save
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
    
