from features.errors import DomainValidationError
from datetime import datetime
from typing import Self


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
        self.exercise_id = exercise_id 
        self.reps_per_set = reps_per_set if reps_per_set is not None else None
        self.weight_per_set = weight_per_set if weight_per_set is not None else None
        self.duration_per_set = duration_per_set if duration_per_set is not None else None

        self.validate()

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Exercise):
            return False
        return self.__dict__ == other.__dict__

    def _validate_metrics(self):
        if not any([self.reps_per_set, self.duration_per_set]):
            raise DomainValidationError("Exercise must have reps or duration")

        if self.reps_per_set and self.weight_per_set:
            if len(self.reps_per_set) != len(self.weight_per_set):
                raise DomainValidationError("Reps and weight length mismatch")
            for rep in self.reps_per_set:
                if rep < 0:
                    raise DomainValidationError("Reps cant be negative.")
            for weight in self.weight_per_set:
                if weight < 0:
                    raise DomainValidationError("Weight cant be negative.")
        
        if self.duration_per_set:
            for duration in self.duration_per_set:
                if duration <= 0:
                    raise DomainValidationError("Duration has to be greater than zero.")
                
    def _validate_name(self):
        if len(self.name.strip()) < 2:
            raise DomainValidationError("Exercise name must be at least two characters long.")
        
    def validate(self):
        self._validate_metrics()
        self._validate_name()

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
        self, 
        routine_id: int, 
        routine_name: str, 
        exercises: list[Exercise], 
        date: str | None = None, 
        session_id: int | None = None
    ):
        self.routine_id = routine_id
        self.routine_name = routine_name
        self.exercises = exercises
        self.date = date if date else datetime.now().replace(second=0, minute=0, microsecond=0).isoformat()
        self.session_id = session_id if session_id else None

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Session):
            return False
        return self.__dict__ == other.__dict__

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