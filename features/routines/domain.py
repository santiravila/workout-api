from features.errors import DomainValidationError
from typing import Self


class Exercise:
    def __init__(
            self, 
            name: str, 
            exercise_id: int | None = None,
            reps_per_set: list[int] | None = None,
            weight_per_set: list[float] | None = None, 
            duration_per_set: list[int] | None = None, 
    ):     
        self.name = name
        self.exercise_id = exercise_id if exercise_id is not  None else None 
        self.reps_per_set = reps_per_set if reps_per_set is not None else None
        self.weight_per_set = weight_per_set if weight_per_set is not None  else None
        self.duration_per_set = duration_per_set if duration_per_set is not  None else None

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


class Routine:
    def __init__(
        self, 
        name: str, 
        exercises: list[Exercise], 
        routine_id: int | None = None
    ):
        self.name = name
        self.exercises = exercises 
        self.routine_id = routine_id if routine_id is not None else None

        self.validate()

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Routine):
            return False
        return self.__dict__ == other.__dict__

    def validate(self):
        if len(self.name.strip()) < 2:
            raise DomainValidationError("Routine name must be at least two characters long.")
        if self.exercises == []:
            raise DomainValidationError("Routine must have exercises")

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        data["exercises"] = [
            Exercise.from_dict(exercise) for exercise in data["exercises"]
        ]
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "exercises": [exercise.to_dict() for exercise in self.exercises],
            "routine_id": self.routine_id
        }    