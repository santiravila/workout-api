from typing import Self
from pydantic import BaseModel
from features.sessions.domain import Exercise, Session 


class ExerciseBase(BaseModel):
    name: str
    exercise_id: int
    reps_per_set: list[int] | None = None
    weight_per_set: list[float] | None = None
    duration_per_set: list[int] | None = None


class ExerciseCreate(ExerciseBase):
    def to_domain(self) -> Exercise:
        return Exercise(
            name=self.name,
            exercise_id=self.exercise_id,
            reps_per_set=self.reps_per_set,
            weight_per_set=self.weight_per_set,
            duration_per_set=self.duration_per_set,
        )


class ExerciseRead(ExerciseBase):
    exercise_id: int

    @classmethod
    def from_domain(cls, exercise: Exercise) -> Self:
        assert exercise.exercise_id is not None, "Routine must be persisted before mapping"

        return cls(
            name=exercise.name,
            exercise_id=exercise.exercise_id,
            reps_per_set=exercise.reps_per_set,
            weight_per_set=exercise.weight_per_set,
            duration_per_set=exercise.duration_per_set
        )



class SessionBase(BaseModel):
    routine_id: int
    routine_name: str
    exercises: list[ExerciseBase]


class SessionCreate(SessionBase):
    exercises: list[ExerciseCreate]

    def to_domain(self) -> Session:
        return Session(
            routine_id=self.routine_id,
            routine_name=self.routine_name,
            exercises=[exercise.to_domain() for exercise in self.exercises],
        )


class SessionRead(SessionBase):
    exercises: list[ExerciseRead]
    session_id: int
    date: str

    @classmethod
    def from_domain(cls, session: Session) -> Self:
        assert session.session_id is not None, "Session must be persisted before mapping"

        return cls( 
            routine_id=session.routine_id,
            routine_name=session.routine_name,
            exercises=[ExerciseRead.from_domain(exercise) for exercise in session.exercises],
            session_id=session.session_id,
            date=session.date,
        )


class SessionUpdate(SessionBase):
    routine_id: int | None = None
    routine_name: str | None = None
    exercises: list[ExerciseBase] | None = None
