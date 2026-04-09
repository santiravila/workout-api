import itertools
import pytest
from features.routines.domain import Routine, Exercise, DomainValidationError


@pytest.fixture
def make_exercise():
    counter = itertools.count(1)

    def _factory(
        name: str = "push-ups", 
        exercise_id: int | None = None, 
        **kwargs
    ):
        if "reps_per_set" not in kwargs and "duration_per_set" not in kwargs:
            kwargs["reps_per_set"] = [10, 10, 10]
            
        return Exercise(
            name=name, 
            exercise_id=exercise_id if exercise_id is not None else next(counter), 
            **kwargs
        )
    return _factory


@pytest.fixture
def make_routine(make_exercise):
    counter = itertools.count(1)

    def _factory(
        name: str = "strength",
        exercises: list[Exercise] = [make_exercise(), make_exercise()],
        routine_id: int | None = None,
        **kwargs,
    ):
        return Routine(
            name=name,
            exercises=exercises,
            routine_id=routine_id if routine_id is not None else next(counter),
            **kwargs,
        )
    return _factory


def test_exercise_raises_without_reps_or_duration(make_exercise):
    with pytest.raises(DomainValidationError) as exc:
        make_exercise(reps_per_set=None, duration_per_set=None)
    assert "Exercise must have reps or duration" in str(exc.value)


def test_exercise_raises_with_reps_weight_mismatch(make_exercise):
    with pytest.raises(DomainValidationError) as exc:
        make_exercise(reps_per_set=[1, 2, 3], weight_per_set=[1.0, 2.0])
    assert "Reps and weight length mismatch" in str(exc.value)


def test_routine_contains_all_added_exercises(make_exercise, make_routine):
    exercises = [make_exercise(), make_exercise()]
    routine = make_routine(exercises=exercises)
    assert all(ex in routine.exercises for ex in exercises)


# implement Exercise __eq__ for this
def test_routine_dict_roundtrips(make_exercise, make_routine):
    original = make_routine(
        name="strength day",
        exercises=[make_exercise(reps_per_set=[5, 5, 5], weight_per_set=[100.0, 100.0, 100.0])]
    )
    restored = Routine.from_dict(original.to_dict())

    assert restored.name == original.name
    assert len(restored.exercises) == len(original.exercises)
    for original_ex, restored_ex in zip(original.exercises, restored.exercises):
        assert restored_ex.name == original_ex.name
        assert restored_ex.reps_per_set == original_ex.reps_per_set