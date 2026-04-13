import pytest
import itertools
from typing import Callable 
from features.routines.domain import Exercise as RoutineExercise
from features.sessions.domain import Exercise as SessionExercise


@pytest.fixture
def make_exercise_routine() -> Callable[..., RoutineExercise]:
    counter = itertools.count(1)

    def _factory(**kwargs) -> RoutineExercise:
        exercise = RoutineExercise(
            name=kwargs.get("name", "pull-ups"),
            exercise_id=kwargs.get("exercise_id", next(counter)),
            reps_per_set=kwargs.get("reps_per_set", [2,2,2]),
            weight_per_set=kwargs.get("weight_per_set", [5,5,7]),
            duration_per_set=kwargs.get("duration_per_set", None)
        )
        return exercise
    return _factory


@pytest.fixture
def make_exercise_session() -> Callable[..., SessionExercise]:
    counter = itertools.count(1)

    def _factory(**kwargs) -> SessionExercise:
        exercise = SessionExercise(
            name=kwargs.get("name", "pull-ups"),
            exercise_id=kwargs.get("exercise_id", next(counter)),
            reps_per_set=kwargs.get("reps_per_set", [2,2,2]),
            weight_per_set=kwargs.get("weight_per_set", [5,5,7]),
            duration_per_set=kwargs.get("duration_per_set", None)
        )
        return exercise
    return _factory