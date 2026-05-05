import pytest
from typing import Callable
from datetime import datetime

@pytest.fixture
def make_routine_payload() -> Callable[..., dict]:
    def _factory(**kwargs) -> dict:
        payload = {
            "name": "pull day",
            "exercises":[
                {
                    "name": "pullups",
                    "reps_per_set":[10, 10, 10]
                }
            ]
        }

        payload.update(kwargs)
    
        return payload
    
    return _factory

@pytest.fixture
def make_session_payload() -> Callable[..., dict]:
    def _factory(**kwargs) -> dict:
        payload = {
            "routine_id": kwargs.get("routine_id", 0),
            "routine_name": kwargs.get("routine_name", "pull-ups"),
            "exercises": kwargs.get(
                "exercises", 
                [
                    {
                        "exercise_id": 1,
                        "name": "pullups",
                        "reps_per_set":[10, 10, 10]
                    }
                ]
            )
        }

        payload.update(kwargs)
    
        return payload
    
    return _factory