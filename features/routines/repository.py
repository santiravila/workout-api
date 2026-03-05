from features.routines.domain import Routine

# temp mock storage
_ROUTINES: list[Routine] = []
next_id = 1


class RoutineRepository:
    def save_routine(self, routine: Routine) -> Routine:
        global next_id

        routine.id = next_id

        _ROUTINES.append(routine)
        next_id += 1

        return routine


    def get_routine_by_id(self, routine_id: int) -> Routine:
        for routine in _ROUTINES:
            if routine.id == routine_id:
                return routine
        
        raise ValueError(f"Not found")


    def list_routines(self) -> list[Routine]:
        return _ROUTINES
        
    
    def remove_routine(self, routine_id: int) -> Routine:
        for index, routine in enumerate(_ROUTINES):
            if routine.id == routine_id:
                return _ROUTINES.pop(index)
        
        raise ValueError(f"Not found")