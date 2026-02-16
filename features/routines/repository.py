from features.routines.domain import Routine

# temp mock storage
_ROUTINES: list[Routine] = []
next_id = 1

# consider creating a RoutineRepository class for encapsulating related functionality
def save(routine: Routine) -> Routine:
    global next_id

    routine.id = next_id

    _ROUTINES.append(routine)
    next_id += 1

    return routine


def get_by_id(id: int):
    for routine in _ROUTINES:
        if routine.id == id:
            return routine
    
    raise ValueError(f"Routine with id={id} not found")
