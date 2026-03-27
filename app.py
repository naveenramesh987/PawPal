import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Initialize session state once ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", available_minutes=60)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name="", species="dog")
    st.session_state.owner.add_pet(st.session_state.pet)

# --- Section 1: Owner + Pet Profile ---
st.subheader("Owner & Pet Profile")

owner_name     = st.text_input("Owner name", value=st.session_state.owner.name or "Jordan")
available_mins = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=st.session_state.owner.available_minutes)
pet_name       = st.text_input("Pet name", value=st.session_state.pet.name or "Mochi")
species        = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(st.session_state.pet.species))

if st.button("Save profile"):
    st.session_state.owner.name              = owner_name
    st.session_state.owner.available_minutes = available_mins
    st.session_state.pet.name               = pet_name
    st.session_state.pet.species            = species
    st.success(f"Profile saved! {st.session_state.owner.get_summary()}")

st.divider()

# --- Section 2: Add Tasks ---
st.subheader("Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    start_time = st.text_input("Start time (HH:MM)", value="", placeholder="e.g. 08:00")

if st.button("Add task"):
    new_task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority,
        start_time=start_time.strip(),
    )
    st.session_state.pet.add_task(new_task)
    st.success(f"Added: {task_title}")

st.divider()

# --- Section 3: All Tasks Sorted by Time ---
scheduler = Scheduler(st.session_state.owner)
current_tasks = st.session_state.pet.get_tasks()

st.subheader(f"All Tasks — sorted by start time")

if current_tasks:
    sorted_tasks = scheduler.sort_by_time(current_tasks)
    st.table([
        {
            "Start time": t.start_time or "—",
            "Task": t.title,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Done": t.completed,
        }
        for t in sorted_tasks
    ])

    # --- Conflict warnings ---
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts detected.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Section 4: Pending vs Completed ---
st.subheader("Task Status")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("Pending")
    pending = scheduler.filter_by_status(completed=False)
    if pending:
        st.table([{"Task": t.title, "Priority": t.priority} for t in pending])
    else:
        st.success("All tasks complete!")

with col_b:
    st.markdown("Completed")
    done = scheduler.filter_by_status(completed=True)
    if done:
        st.table([{"Task": t.title, "Priority": t.priority} for t in done])
    else:
        st.info("None completed yet.")

st.divider()

# --- Section 5: Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not current_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        plan = scheduler.generate_plan()
        st.success("Schedule generated!")
        st.text(plan.explain())
        st.table(plan.display())
