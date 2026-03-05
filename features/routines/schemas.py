from typing import Self
from pydantic import BaseModel
from features.routines.domain import Routine


class RoutineBase(BaseModel):
    name: str
    #rest_between_sets: int
    #tempo: str
    #exercises: list[Exercise]


class RoutineCreate(RoutineBase):
    def to_domain(self) -> Routine:
        return Routine(
            name=self.name
        )


class RoutineRead(RoutineBase):
    id: int 

    @classmethod
    def from_domain(cls, routine: Routine) -> Self:
        if routine.id is None:
            raise ValueError("Routine must be persisted before mapping")
        
        return cls(
            name=routine.name,
            id=routine.id
        )


class RoutineUpdate(BaseModel):
    name: str | None = None

    
class RoutineExercise(BaseModel):
    name: str
    sets: int
    reps: int | None = None
    weight: float | None = None
    duration: int | None = None