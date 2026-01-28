from datetime import datetime
from copy import deepcopy
import json
from pathlib import Path

DATA_DIR = Path("data")
STORAGE_FILE = DATA_DIR / "storage.json"


class Exercise:
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __init__(
        self, name: str, sets: int, weight: float, reps: list[int] | None = None
    ):
        self.name = name
        self.sets = sets
        self.weight = weight
        self.reps = [] if reps is None else reps

    def __eq__(self, other):
        if not isinstance(other, Exercise):
            return NotImplemented
        return (
            self.name == other.name
            and self.sets == other.sets
            and self.weight == other.weight
            and self.reps == other.reps
        )

    def __str__(self):
        return f"Exercise: {self.name} | Sets: {self.sets} | Weight: {self.weight} | Reps: {self.reps}"

    def to_dict(self):
        return {
            "name": self.name,
            "sets": self.sets,
            "weight": self.weight,
            "reps": self.reps,
        }


class Session:
    @classmethod
    def from_dict(cls, data: dict):
        if "date" in data:
            data["date"] = datetime.fromisoformat(data["date"])

        data["exercises"] = [
            Exercise.from_dict(exercise) for exercise in data["exercises"]
        ]

        return cls(**data)

    def __init__(
        self, id: int, routine_name: str, date: datetime, exercises: list[Exercise]
    ) -> None:
        self.id = id
        self.date = date
        self.exercises = exercises
        self.routine_name = routine_name

    def __str__(self):
        return f"Routine: {self.routine_name}, Workout Date: {self.date}"

    def to_dict(self):
        return {
            "id": self.id,
            "routine_name": self.routine_name,
            "date": self.date.isoformat(),
            "exercises": [exercise.to_dict() for exercise in self.exercises],
        }


class Routine:
    @classmethod
    def from_dict(cls, data: dict):
        data["exercises"] = [
            Exercise.from_dict(exercise) for exercise in data["exercises"]
        ]
        return cls(**data)

    def __init__(
        self, id: int, name: str, rest: float, tempo: str, exercises: list[Exercise]
    ):
        self.id = id
        self.name = name
        self.rest = rest
        self.tempo = tempo
        self.exercises = exercises

    def __eq__(self, other):
        if not isinstance(other, Routine):
            return NotImplemented
        return (
            self.name == other.name
            and self.rest == other.rest
            and self.tempo == other.tempo
            and self.exercises == other.exercises
        )

    def __str__(self):
        return f"Routine: {self.name} | Rest: {self.rest} | Tempo: {self.tempo}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rest": self.rest,
            "tempo": self.tempo,
            "exercises": [exercise.to_dict() for exercise in self.exercises],
        }


class RoutineCreation:
    def __init__(self, manager, name: str):
        if name in [routine.name for routine in manager.get_routines()]:
            raise ValueError("Routine already exists")

        self.manager = manager
        self.name = name

        self.exercises = []
        self.rest = None
        self.tempo = None

    def add_exercise(self, name: str, sets: int, weight: float):
        if sets <= 0:
            raise ValueError("Sets must be positive")

        if weight < 0:
            raise ValueError("Weight cannot be negative")
        exercise = Exercise(name, sets, weight)
        self.exercises.append(exercise)

    def set_rest(self, rest: float):
        if rest < 0:
            raise ValueError("Rest cannot be negative")
        self.rest = rest

    def set_tempo(self, tempo: str):
        if not tempo:
            raise ValueError("Tempo cannot be empty")
        self.tempo = tempo

    def finish(self) -> Routine | None:
        if not self.exercises:
            raise ValueError("Routine must have at least one exercise")

        if self.rest is None or self.tempo is None:
            raise ValueError("Routine is incomplete")

        routine_id = len(self.manager.get_routines()) + 1

        routine = Routine(routine_id, self.name, self.rest, self.tempo, self.exercises)

        self.manager.routines.append(routine)
        return routine


class SessionCreation:
    def __init__(self, manager, routine: Routine):
        self.manager = manager
        self.routine = routine
        self.exercises = deepcopy(routine.exercises)

    def add_reps(self, exercise: Exercise, rep_number: int):
        if rep_number < 0:
            raise ValueError("Reps must be positive")

        for internal_exercise in self.exercises:
            if exercise.name == internal_exercise.name:
                internal_exercise.reps.append(rep_number)

    def finish(self):
        for exercise in self.exercises:
            if exercise.sets != len(exercise.reps):
                raise ValueError(
                    f"Exercise reps: {exercise.reps} do not match number of sets: {exercise.sets}"
                )

        session_id = len(self.manager.sessions) + 1

        session = Session(session_id, self.routine.name, datetime.now(), self.exercises)

        self.manager.sessions.append(session)
        return session


class ReportGenerator:
    def __init__(self, routine: Routine, sessions: list[Session], exercise_index: int):
        self.routine = routine
        self.sessions = sessions
        self.exercise_index = exercise_index
        self.timeline = []
        self.measurements = {}

    def get_timeline(self):
        self.timeline = []
        for session in self.sessions:
            self.timeline.append(session.date)
        return self.timeline

    def get_measurements(self):
        self.measurements = {}
        routine_exercise = self.routine.exercises[self.exercise_index]
        for set in range(1, routine_exercise.sets + 1):
            session_reps = []
            for session in self.sessions:
                exercise = session.exercises[self.exercise_index]
                session_reps.append(exercise.reps[set - 1])
            self.measurements[set] = tuple(session_reps)
        return self.measurements

    def max_measurement(self):
        return max(element for data in self.measurements.values() for element in data)


class AppManager:
    def __init__(self, storage_file=None) -> None:
        self.routines = []
        self.sessions = []

        if storage_file is None:
            self.storage_file = STORAGE_FILE
        else:
            self.storage_file = storage_file

    def start_routine_creation(self, name: str) -> RoutineCreation:
        return RoutineCreation(self, name)

    def start_session_creation(self, routine: Routine) -> SessionCreation:
        return SessionCreation(self, routine)

    def create_report(self, routine, sessions, exercise_index):
        return ReportGenerator(routine, sessions, exercise_index)

    def get_routines(self):
        return self.routines

    def get_sessions(self):
        return self.sessions

    def get_routine(self, index: int) -> Routine:
        for routine in self.routines:
            if routine.id == index:
                return deepcopy(routine)
        raise ValueError(f"No routine of index: {index}")

    def save_data(self):
        data = {
            "routines": [r.to_dict() for r in self.routines],
            "sessions": [s.to_dict() for s in self.sessions],
        }

        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        # Ensure the data directory exists
        DATA_DIR.mkdir(exist_ok=True)

        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)

            for routine in data["routines"]:
                loaded_routine = Routine.from_dict(routine)
                if loaded_routine is not None:
                    self.routines.append(loaded_routine)

            for session in data["sessions"]:
                loaded_session = Session.from_dict(session)
                if loaded_session is not None:
                    self.sessions.append(loaded_session)
        except FileNotFoundError as e:
            print(e)
