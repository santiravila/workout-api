from datetime import datetime
from typing import Self


class Exercise:
    #def __init__(self, name: str, sets: int, weight: float, reps: list[int], exercise_id: int):
    def __init__(self, name: str, exercise_id: int):
     
        self.name = name
        #self.sets = sets
        #self.weight = weight
        #self.reps = reps
        self.exercise_id = exercise_id

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
          #  "sets": self.sets,
          #  "weight": self.weight,
          #  "reps": self.reps,
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
