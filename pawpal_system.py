from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str              # "low", "medium", "high"
    category: str = ""
    is_required: bool = False

    def is_high_priority(self) -> bool:
        pass

    def __repr__(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = None
    notes: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list:
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: str = ""):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_summary(self) -> str:
        pass


class DailyPlan:
    def __init__(self, scheduled_tasks: list, skipped_tasks: list, total_minutes_used: int):
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.total_minutes_used = total_minutes_used
        self.generated_at = datetime.now()

    def explain(self) -> str:
        pass

    def display(self) -> list:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks = pet.get_tasks()

    def generate_plan(self) -> DailyPlan:
        pass

    def _sort_tasks(self) -> list:
        pass

    def _fits_in_time(self, task: Task, remaining_minutes: int) -> bool:
        pass
