from pydantic import BaseModel
#from schemas.exercise import Exercise


class RoutineBase(BaseModel):
    name: str
    #rest_between_sets: int
    #tempo: str
    #exercises: list[Exercise]


class RoutineCreate(RoutineBase):
    pass


class RoutineRead(RoutineBase):
    id: int 


class RoutineExercise(BaseModel):
    name: str
    sets: int
    reps: int | None = None
    weight: float | None = None
    duration: int | None = None