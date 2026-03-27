# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Beyond the basic daily plan, the scheduler includes four additional features:

- Sort by time — tasks can be ordered by their `start_time` field (HH:MM), with unscheduled tasks pushed to the end.
- Filter by status — retrieve only pending or only completed tasks across all pets.
- Filter by pet — retrieve all tasks belonging to a specific pet by name.
- Recurring tasks — when a daily or weekly task is marked complete, a new instance is automatically created for the next occurrence using `timedelta`.
- Conflict detection — warns when two tasks (across any pet) share the exact same start time, helping the owner catch scheduling collisions before they happen.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite contains 5 tests covering:

- Task completion — verifies that `mark_complete()` flips `completed` from `False` to `True`
- Task addition — verifies that `add_task()` increases the pet's task count
- Sorting correctness — verifies that `sort_by_time()` returns tasks in chronological order (07:00 → 08:00 → 15:00)
- Recurrence logic — verifies that completing a daily task creates a new task due the following day
- Conflict detection — verifies that `detect_conflicts()` flags two tasks sharing the same start time

Confidence level: ★★★★☆

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
