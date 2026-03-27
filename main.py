from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

# --- Tasks for Mochi ---
mochi.add_task(Task(title="Morning walk",   duration_minutes=30, priority="high",   is_required=True))
mochi.add_task(Task(title="Feeding",        duration_minutes=10, priority="high",   is_required=True))
mochi.add_task(Task(title="Fetch session",  duration_minutes=20, priority="medium", category="enrichment"))

# --- Tasks for Luna ---
luna.add_task(Task(title="Medication",      duration_minutes=5,  priority="high",   is_required=True))
luna.add_task(Task(title="Brushing",        duration_minutes=15, priority="medium", category="grooming"))
luna.add_task(Task(title="Laser toy play",  duration_minutes=10, priority="low",    category="enrichment"))

# --- Add pets to owner ---
owner.add_pet(mochi)
owner.add_pet(luna)

# --- Generate plan ---
scheduler = Scheduler(owner)
plan = scheduler.generate_plan()

# --- Print schedule ---
print("=" * 45)
print("        TODAY'S SCHEDULE")
print("=" * 45)
print(plan.explain())
print("=" * 45)
