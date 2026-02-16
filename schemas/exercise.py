from pydantic import BaseModel


class Exercise(BaseModel):
    name: str
    sets: int
    reps: int | None = None
    weight: float | None = None
    duration: int | None = None