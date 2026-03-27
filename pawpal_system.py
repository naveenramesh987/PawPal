from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str                  # "low", "medium", "high"
    category: str = ""
    frequency: str = "daily"       # "daily", "weekly", "as needed"
    is_required: bool = False
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is high."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False


@dataclass
class Pet:
    name: str
    species: str
    age: int = None
    notes: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def get_pending_tasks(self) -> list:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: str = ""):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        """Return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_summary(self) -> str:
        """Return a one-line summary of the owner's name, time budget, and pets."""
        pet_names = ", ".join(p.name for p in self.pets) if self.pets else "none"
        return (
            f"Owner: {self.name} | "
            f"Available: {self.available_minutes} min/day | "
            f"Pets: {pet_names}"
        )


class DailyPlan:
    def __init__(self, owner: "Owner", scheduled_tasks: list, skipped_tasks: list, total_minutes_used: int):
        self.owner = owner
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.total_minutes_used = total_minutes_used
        self.generated_at = datetime.now()

    def explain(self) -> str:
        """Return a human-readable summary of scheduled and skipped tasks."""
        lines = [
            f"Plan for {self.owner.name} — {self.generated_at.strftime('%B %d, %Y')}",
            f"Time available: {self.owner.available_minutes} min | Time used: {self.total_minutes_used} min",
            "",
            "Scheduled:",
        ]
        for task in self.scheduled_tasks:
            reason = "required" if task.is_required else f"{task.priority} priority"
            lines.append(f"  - {task.title} ({task.duration_minutes} min) — {reason}")

        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped (not enough time):")
            for task in self.skipped_tasks:
                lines.append(f"  - {task.title} ({task.duration_minutes} min)")

        return "\n".join(lines)

    def display(self) -> list:
        """Return scheduled tasks as a list of dicts, suitable for st.table()."""
        return [
            {
                "Task": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Required": t.is_required,
                "Done": t.completed,
            }
            for t in self.scheduled_tasks
        ]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> list:
        """Retrieve every task across all of the owner's pets."""
        return self.owner.get_all_tasks()

    def generate_plan(self) -> DailyPlan:
        """Select and order tasks that fit within the owner's available time."""
        sorted_tasks = self._sort_tasks()
        remaining = self.owner.available_minutes
        scheduled = []
        skipped = []

        for task in sorted_tasks:
            if self._fits_in_time(task, remaining):
                scheduled.append(task)
                remaining -= task.duration_minutes
            else:
                skipped.append(task)

        total_used = self.owner.available_minutes - remaining
        return DailyPlan(self.owner, scheduled, skipped, total_used)

    def _sort_tasks(self) -> list:
        """Sort tasks: required first, then by priority (high → medium → low)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            self.get_all_tasks(),
            key=lambda t: (0 if t.is_required else 1, priority_order.get(t.priority, 3))
        )

    def _fits_in_time(self, task: Task, remaining_minutes: int) -> bool:
        """Return True if the task's duration fits within the remaining time."""
        return task.duration_minutes <= remaining_minutes
