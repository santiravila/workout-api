from fastapi import APIRouter
from features.routines.schemas import RoutineCreate, RoutineRead, RoutineUpdate
from features.routines.controller import RoutineController


router = APIRouter(prefix="/routines", tags=["routines"])
controller = RoutineController()


@router.post("/", response_model=RoutineRead)
def create_routine(payload: RoutineCreate) -> RoutineRead:
    """
    params: input routine as RoutineCreate DTO

    return: RoutineRead DTO 
    
    appends a new routine object to a list in repository and returns the created routine.
    """
    return controller.create_routine(payload)


@router.get("/{id}", response_model=RoutineRead)
def get_routine(id: int) -> RoutineRead:
    return controller.get_routine(id)


@router.get("/", response_model=list[RoutineRead])
def get_routines() -> list[RoutineRead]:
    return controller.list_routines_controller()


@router.patch("/{id}", response_model=RoutineRead)
def update_routine(id: int, payload: RoutineUpdate) -> RoutineRead:
    return controller.update_routine(id, payload)