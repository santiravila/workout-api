from typing import Self
from pydantic import BaseModel
from features.sessions.domain import Exercise, Session 


class ExerciseBase(BaseModel):
    exercise_id: int
    name: str


class ExerciseCreate(ExerciseBase):
    def to_domain(self) -> Exercise:
        return Exercise(
            name=self.name,
            exercise_id=self.exercise_id,
        )


class ExerciseRead(ExerciseBase):
    @classmethod
    def from_domain(cls, exercise: Exercise) -> Self:
        return cls(
            name=exercise.name,
            exercise_id=exercise.exercise_id,
        )


class SessionBase(BaseModel):
    routine_id: int
    routine_name: str


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
        if session.session_id is None:
            raise  ValueError("Session must be persisted before mapping")

        return cls(
            routine_id=session.routine_id,
            routine_name=session.routine_name,
            exercises=[ExerciseRead.from_domain(exercise) for exercise in session.exercises],
            session_id=session.session_id,
            date=session.date,
        )


class SessionUpdate(SessionBase):
    ...
