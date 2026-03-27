from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Fetch", duration_minutes=20, priority="medium", start_time="15:00"))
    pet.add_task(Task(title="Walk",  duration_minutes=30, priority="high",   start_time="07:00"))
    pet.add_task(Task(title="Feed",  duration_minutes=10, priority="high",   start_time="08:00"))

    owner = Owner(name="Jordan", available_minutes=90)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()
    times = [t.start_time for t in sorted_tasks]
    assert times == ["07:00", "08:00", "15:00"]


def test_complete_task_creates_next_day_occurrence():
    today = date.today()
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily", due_date=today)
    pet.add_task(task)

    owner = Owner(name="Jordan", available_minutes=90)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    next_task = scheduler.complete_task(task, pet)

    assert task.completed == True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert len(pet.get_tasks()) == 2


def test_detect_conflicts_flags_shared_start_time():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Feeding",   duration_minutes=10, priority="high", start_time="08:00"))
    pet.add_task(Task(title="Medication", duration_minutes=5,  priority="high", start_time="08:00"))

    owner = Owner(name="Jordan", available_minutes=90)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
