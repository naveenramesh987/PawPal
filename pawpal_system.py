from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str                  # "low", "medium", "high"
    category: str = ""
    frequency: str = "daily"       # "daily", "weekly", "as needed"
    is_required: bool = False
    completed: bool = False
    start_time: str = ""           # "HH:MM" format, e.g. "08:30"
    due_date: date = field(default_factory=date.today)

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is high."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def next_due_date(self) -> date | None:
        """Return the next due date based on frequency, or None if non-recurring."""
        if self.frequency == "daily":
            return self.due_date + timedelta(days=1)
        if self.frequency == "weekly":
            return self.due_date + timedelta(weeks=1)
        return None  # "as needed" tasks do not recur automatically


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

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by start_time (HH:MM); tasks with no time set go last."""
        source = tasks if tasks is not None else self.get_all_tasks()
        return sorted(
            source,
            key=lambda t: t.start_time if t.start_time else "99:99"
        )

    def filter_by_status(self, completed: bool) -> list:
        """Return tasks matching the given completion status across all pets."""
        return [t for t in self.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list:
        """Return all tasks belonging to the pet with the given name."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def detect_conflicts(self) -> list[str]:
        """Return a list of warning strings for any tasks that share the same start time."""
        time_slots: defaultdict[str, list[str]] = defaultdict(list)
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                if not task.start_time:
                    continue
                time_slots[task.start_time].append(f"{task.title} ({pet.name})")

        warnings = []
        for time, names in time_slots.items():
            if len(names) > 1:
                warnings.append(
                    f"WARNING: Conflict at {time} — {' and '.join(names)} are scheduled at the same time."
                )
        return warnings

    def complete_task(self, task: Task, pet: Pet) -> Task | None:
        """Mark a task complete and add the next occurrence to the pet if it recurs."""
        task.mark_complete()
        next_date = task.next_due_date()
        if next_date is None:
            return None
        next_task = Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            category=task.category,
            frequency=task.frequency,
            is_required=task.is_required,
            start_time=task.start_time,
            due_date=next_date,
        )
        pet.add_task(next_task)
        return next_task
