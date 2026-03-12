from typing import Self


class Exercise:
    #def __init__(self, name: str, sets: int, weight: float, reps: list[int], id: int | None = None):
    def __init__(self, name: str, id: int | None = None):
     
        self.name = name
        #self.sets = sets
        #self.weight = weight
        #self.reps = reps
        self.id = id if id else None 

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
          #  "sets": self.sets,
          #  "weight": self.weight,
          #  "reps": self.reps,
            "id": self.id
        }


class Routine:
    def __init__(self, name: str, exercises: list[Exercise], id: int | None = None):
        self.name = name
        self.exercises = exercises 
        self.id = id

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
            "id": self.id
        }    