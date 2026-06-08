from typing import Annotated
from fastapi import Depends
from .repository import RoutineRepository
from .service import RoutineService


def get_routine_service() -> RoutineService:
    repo = RoutineRepository()
    return RoutineService(repo=repo)


ServiceDep = Annotated[
    RoutineService, 
    Depends(get_routine_service)
]