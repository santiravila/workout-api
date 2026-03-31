from fastapi import APIRouter, Depends
from typing import Annotated
from features.routines.schemas import RoutineCreate, RoutineRead, RoutineUpdate
from features.routines.repository import RoutineRepository
from features.routines.controller import RoutineController


router = APIRouter(prefix="/api/v1/routines", tags=["routines"])

def get_routine_controller() -> RoutineController:
    repo = RoutineRepository()
    return RoutineController(repo=repo)

ControllerDep = Annotated[RoutineController, Depends(get_routine_controller)]

@router.post("/", response_model=RoutineRead)
def create_routine(
    payload: RoutineCreate,
    controller: ControllerDep
) -> RoutineRead:
    return controller.create_routine(payload)


@router.get("/{id}", response_model=RoutineRead)
def get_routine(
    id: int,
    controller: ControllerDep
) -> RoutineRead:
    return controller.get_routine(id)


@router.get("/", response_model=list[RoutineRead])
def get_routines(
    controller: ControllerDep
) -> list[RoutineRead]:
    return controller.list_routines_controller()


@router.patch("/{id}", response_model=RoutineRead)
def update_routine(
    id: int, 
    payload: RoutineUpdate,
    controller: ControllerDep
) -> RoutineRead:
    return controller.update_routine(id, payload)


@router.delete("/{id}", response_model=RoutineRead)
def delete_routine(
    id: int,
    controller: ControllerDep
) -> RoutineRead:
    return controller.delete_routine(id)