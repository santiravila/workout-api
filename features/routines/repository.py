from features.routines.domain import Routine

# temp mock storage
_ROUTINES: list[Routine] = []
next_id = 1


class RoutineRepository:
    def save(self, routine: Routine) -> Routine:
        global next_id

        routine.id = next_id

        _ROUTINES.append(routine)
        next_id += 1

        return routine


    def get_by_id(self, routine_id: int) -> Routine:
        for routine in _ROUTINES:
            if routine.id == routine_id:
                return routine
        
        raise ValueError(f"Not found")


    def list_routines(self) -> list[Routine]:
        return _ROUTINES
        