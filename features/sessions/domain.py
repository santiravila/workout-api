from datetime import datetime
from typing import Self


class DomainValidationError(Exception):
    pass


class Exercise:
    def __init__(
            self, 
            name: str, 
            exercise_id: int,
            reps_per_set: list[int] | None = None,
            weight_per_set: list[float] | None = None, 
            duration_per_set: list[int] | None = None, 
    ):     
        self.name = name
        self.reps_per_set = reps_per_set if reps_per_set else None
        self.weight_per_set = weight_per_set if weight_per_set else None
        self.duration_per_set = duration_per_set if duration_per_set else None
        self.exercise_id = exercise_id 

        self.validate()

    def validate(self):
        if not any([self.reps_per_set, self.duration_per_set]):
            raise DomainValidationError("Exercise must have reps or duration")

        if self.reps_per_set and self.weight_per_set:
            if len(self.reps_per_set) != len(self.weight_per_set):
                raise DomainValidationError("Reps and weight length mismatch")

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "reps_per_set": self.reps_per_set,
            "weight_per_set": self.weight_per_set,
            "duration_per_set": self.duration_per_set,
            "exercise_id": self.exercise_id
        }

    

class Session:
    def __init__(
        self, routine_id: int, routine_name: str, exercises: list[Exercise], date: str | None = None, session_id: int | None = None
    ) -> None:
        self.routine_id = routine_id
        self.routine_name = routine_name
        self.exercises = exercises
        self.date = date if date else datetime.now().replace(second=0, minute=0, microsecond=0).isoformat()
        self.session_id = session_id if session_id else None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        data["exercises"] = [
            Exercise.from_dict(exercise) for exercise in data["exercises"]
        ]
        return cls(**data)    

    def to_dict(self) -> dict:
        return {
            "routine_id": self.routine_id,
            "routine_name": self.routine_name,
            "exercises": [exercise.to_dict() for exercise in self.exercises],
            "date": self.date,
            "session_id": self.session_id,
        }

    def apply_patch(self, data: dict) -> None:
        for key, value in data.items():
            if key == "exercises":
                self.exercises = [
                    Exercise.from_dict(ex) for ex in value
                ]
            else:
                setattr(self, key, value)