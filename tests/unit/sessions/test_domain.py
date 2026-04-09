import pytest
from datetime import datetime
import itertools
from features.sessions.domain import Session, Exercise, DomainValidationError

@pytest.fixture
def make_exercise():
    count = itertools.count(1)

    def _factory(
        name: str = "push-ups",
        exercise_id: int | None = None,
        **kwargs
    ):
        if "reps_per_set" not in kwargs and "duration_per_set" not in kwargs:
            kwargs["reps_per_set"] = [10, 10, 10]
        
        return Exercise(
            name=name,
            exercise_id=exercise_id if exercise_id is not None else next(count),
            **kwargs
        )
    return _factory


@pytest.fixture
def make_session(make_exercise):
    count = itertools.count(1)

    def _factory(
        session_id: int | None = None,
        routine_id: int = 1,
        routine_name: str = "push day",
        exercises: list[Exercise] = [make_exercise(), make_exercise()],
        date: str = datetime.now().replace(second=0, minute=0, microsecond=0).isoformat()
    ):
        return Session(
            routine_id==routine_id,
            routine_name=routine_name,
            exercises=exercises,
            date=date,
            session_id=session_id if session_id is not None else next(count)
        )
    return _factory


def test_exercise_raises_without_reps_or_duration(make_exercise):
    with pytest.raises(DomainValidationError) as exception_info:
        make_exercise(reps_per_set=None, duration_per_set=None)
    assert "Exercise must have reps or duration" in str(exception_info.value)


def test_exercise_raises_with_reps_weight_mismatch(make_exercise):
    with pytest.raises(DomainValidationError) as exception_info:
        make_exercise(reps_per_set=[1,1,1], weight_per_set=[1,1])
    assert "Reps and weight length mismatch" in str(exception_info.value)


def test_sessions_dict_roundtrips(make_session):
    original = make_session()
    restored = Session.from_dict(original.to_dict())

    assert original.routine_name == restored.routine_name
    assert len(original.exercises) == len(restored.exercises)
    for original_ex, restored_ex in zip(original.exercises, restored.exercises):
        assert original_ex.name == restored_ex.name
        assert original_ex.reps_per_set == restored_ex.reps_per_set
