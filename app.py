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

owner_name      = st.text_input("Owner name", value=st.session_state.owner.name or "Jordan")
available_mins  = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=st.session_state.owner.available_minutes)
pet_name        = st.text_input("Pet name", value=st.session_state.pet.name or "Mochi")
species         = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(st.session_state.pet.species))

if st.button("Save profile"):
    st.session_state.owner.name              = owner_name
    st.session_state.owner.available_minutes = available_mins
    st.session_state.pet.name               = pet_name
    st.session_state.pet.species            = species
    st.success(f"Profile saved! {st.session_state.owner.get_summary()}")

st.divider()

# --- Section 2: Add Tasks ---
st.subheader("Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    new_task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
    st.session_state.pet.add_task(new_task)   # <- pet.add_task() handles storing it
    st.success(f"Added: {task_title}")

current_tasks = st.session_state.pet.get_tasks()
if current_tasks:
    st.write(f"Tasks for {st.session_state.pet.name or 'your pet'}:")
    st.table([
        {"Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
        for t in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Section 3: Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.pet.get_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        plan = scheduler.generate_plan()
        st.success("Schedule generated!")
        st.text(plan.explain())
        st.table(plan.display())
