import itertools
import pytest
from typing import Callable
from features.routines.domain import Routine, DomainValidationError


@pytest.fixture
def make_routine(make_exercise_routine) -> Callable[..., Routine]:
    counter = itertools.count(1)

    def _factory(**kwargs,) -> Routine:
        routine = Routine(
            name=kwargs.get("name", "pull-day"),
            exercises=kwargs.get("exercises", [make_exercise_routine(), make_exercise_routine()]),
            routine_id=kwargs.get("routine_id", next(counter))
        )
        return routine
    return _factory


def test_exercise_raises_without_reps_or_duration(make_exercise_routine):
    with pytest.raises(DomainValidationError) as exc:
        make_exercise_routine(reps_per_set=None, duration_per_set=None)
    assert "Exercise must have reps or duration" in str(exc.value)


def test_exercise_raises_with_incorrect_name(make_exercise_routine):
    with pytest.raises(DomainValidationError):
        make_exercise_routine(name="")
    

def test_exercise_raises_with_negative_reps(make_exercise_routine):
    with pytest.raises(DomainValidationError):
        make_exercise_routine(reps_per_set=[1, 2, 3, -1])
    

def test_exercise_raises_with_negative_weight(make_exercise_routine):
    with pytest.raises(DomainValidationError):
        make_exercise_routine(weight_per_set=[1, 2, 3, -1])


def test_exercise_raises_with_non_positive_duration(make_exercise_routine):
    with pytest.raises(DomainValidationError):
        make_exercise_routine(duration_per_set=[1, 0, -1])


def test_exercise_raises_with_reps_weight_mismatch(make_exercise_routine):
    with pytest.raises(DomainValidationError) as exc:
        make_exercise_routine(reps_per_set=[1, 2, 3], weight_per_set=[1.0, 2.0])
    assert "Reps and weight length mismatch" in str(exc.value)


def test_routine_raises_with_incorrect_name(make_routine):
    with pytest.raises(DomainValidationError):
        make_routine(name="")


def test_routine_raises_with_empty_exercises(make_routine):
    with pytest.raises(DomainValidationError):
        make_routine(exercises=[])


def test_routine_contains_all_added_exercises(make_exercise_routine, make_routine):
    exercises = [make_exercise_routine(), make_exercise_routine()]
    routine = make_routine(exercises=exercises)
    assert all(ex in routine.exercises for ex in exercises)


def test_routine_dict_roundtrips(make_routine):
    original = make_routine()
    restored = Routine.from_dict(original.to_dict())

    assert original == restored
