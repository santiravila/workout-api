from typing import Self
from pydantic import BaseModel
from features.routines.domain import Exercise, Routine


class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    def to_domain(self) -> Exercise:
        return Exercise(
            name=self.name,
        )


class ExerciseRead(ExerciseBase):
    exercise_id: int

    @classmethod
    def from_domain(cls, exercise: Exercise) -> Self:

        assert exercise.exercise_id is not None, "Routine must be persisted before mapping"

        return cls(
            name=exercise.name,
            exercise_id=exercise.exercise_id,
        )


class RoutineBase(BaseModel):
    exercises: list[ExerciseBase] 
    name: str


class RoutineCreate(RoutineBase):
    exercises: list[ExerciseCreate] # override base for accesing to_domain, which doesnt have to know about ID

    def to_domain(self) -> Routine:
        return Routine(
            name=self.name,
            exercises=[exercise.to_domain() for exercise in self.exercises],
        )


class RoutineRead(RoutineBase):
    exercises: list[ExerciseRead] # override base for accesing from_domain which considers ID
    id: int 

    @classmethod
    def from_domain(cls, routine: Routine) -> Self:
        if routine.routine_id is None:
            raise ValueError("Routine must be persisted before mapping")
        
        return cls(
            name=routine.name,
            id=routine.routine_id,
            exercises=[ExerciseRead.from_domain(exercise) for exercise in routine.exercises]
        )


class RoutineUpdate(BaseModel):
    name: str | None = None
    