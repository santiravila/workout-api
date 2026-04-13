import itertools
import pytest
from datetime import datetime
from typing import Callable
from features.sessions.domain import Session, DomainValidationError


@pytest.fixture
def make_session(make_exercise_session) -> Callable[..., Session]:
    counter = itertools.count(1)

    def _factory(**kwargs) -> Session:
        session = Session(
            routine_id=kwargs.get("routine_id", 1),
            routine_name=kwargs.get("routine_name", "push day"),
            exercises=kwargs.get("exercises", [make_exercise_session(), make_exercise_session()]),
            date=kwargs.get("date", datetime.now().replace(second=0, minute=0, microsecond=0).isoformat()),
            session_id=kwargs.get("session_id", next(counter)),
        )
        return session
    return _factory


# Had to copy-paste the exact same 4 tests for exercises here from tests/unit/routines/test_domain.py probably time for conftests.py
def test_exercise_raises_with_incorrect_name(make_exercise_session):
    with pytest.raises(DomainValidationError):
        make_exercise_session(name="")
    

def test_exercise_raises_with_negative_reps(make_exercise_session):
    with pytest.raises(DomainValidationError):
        make_exercise_session(reps_per_set=[1, 2, 3, -1])
    

def test_exercise_raises_with_negative_weight(make_exercise_session):
    with pytest.raises(DomainValidationError):
        make_exercise_session(weight_per_set=[1, 2, 3, -1])


def test_exercise_raises_with_non_positive_duration(make_exercise_session):
    with pytest.raises(DomainValidationError):
        make_exercise_session(duration_per_set=[1, 0, -1])


def test_exercise_raises_without_reps_or_duration(make_exercise_session):
    with pytest.raises(DomainValidationError) as exception_info:
        make_exercise_session(reps_per_set=None, duration_per_set=None)


def test_exercise_raises_with_reps_weight_mismatch(make_exercise_session):
    with pytest.raises(DomainValidationError) as exception_info:
        make_exercise_session(reps_per_set=[1,1,1], weight_per_set=[1,1])


def test_sessions_dict_roundtrips(make_session):
    original = make_session()
    restored = Session.from_dict(original.to_dict())

    assert original == restored