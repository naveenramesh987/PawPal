from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog", age=3)
luna  = Pet(name="Luna",  species="cat", age=5)

# --- Tasks added OUT OF ORDER (intentionally scrambled start_times) ---
mochi.add_task(Task(title="Fetch session",  duration_minutes=20, priority="medium", category="enrichment", start_time="15:00"))
mochi.add_task(Task(title="Morning walk",   duration_minutes=30, priority="high",   is_required=True,       start_time="07:00"))
mochi.add_task(Task(title="Feeding",        duration_minutes=10, priority="high",   is_required=True,       start_time="08:00"))

luna.add_task(Task(title="Laser toy play",  duration_minutes=10, priority="low",    category="enrichment",  start_time="18:00"))
luna.add_task(Task(title="Medication",      duration_minutes=5,  priority="high",   is_required=True,       start_time="08:00"))
luna.add_task(Task(title="Brushing",        duration_minutes=15, priority="medium", category="grooming",    start_time="11:00", completed=True))

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner)

# --- Today's Schedule ---
plan = scheduler.generate_plan()
print("=" * 45)
print("         TODAY'S SCHEDULE")
print("=" * 45)
print(plan.explain())

# --- Sort by time ---
print("\n" + "=" * 45)
print("   ALL TASKS SORTED BY START TIME")
print("=" * 45)
for t in scheduler.sort_by_time():
    time_label = t.start_time if t.start_time else "no time set"
    print(f"  {time_label}  {t.title} ({t.duration_minutes} min)")

# --- Filter: pending tasks only ---
print("\n" + "=" * 45)
print("   PENDING TASKS (not yet completed)")
print("=" * 45)
for t in scheduler.filter_by_status(completed=False):
    print(f"  - {t.title}")

# --- Filter: completed tasks only ---
print("\n" + "=" * 45)
print("   COMPLETED TASKS")
print("=" * 45)
done = scheduler.filter_by_status(completed=True)
if done:
    for t in done:
        print(f"  - {t.title}")
else:
    print("  None completed yet.")

# --- Filter: tasks for a specific pet ---
print("\n" + "=" * 45)
print("   LUNA'S TASKS")
print("=" * 45)
for t in scheduler.filter_by_pet("Luna"):
    status = "done" if t.completed else "pending"
    print(f"  - {t.title} [{status}]")

print("=" * 45)

# --- Recurring Task Demo ---
print("\n" + "=" * 45)
print("   RECURRING TASK DEMO")
print("=" * 45)
feeding = mochi.get_tasks()[2]
print(f"Before: '{feeding.title}' due {feeding.due_date}, completed={feeding.completed}")
print(f"Mochi task count before: {len(mochi.get_tasks())}")

next_task = scheduler.complete_task(feeding, mochi)

print(f"After:  '{feeding.title}' completed={feeding.completed}")
print(f"Next occurrence due: {next_task.due_date}  (today + 1 day)")
print(f"Mochi task count after: {len(mochi.get_tasks())}")
print("=" * 45)

# --- Conflict Detection ---
print("\n" + "=" * 45)
print("   CONFLICT DETECTION")
print("=" * 45)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")
print("=" * 45)
