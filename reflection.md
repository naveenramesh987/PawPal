# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

1. Add a pet profile

2. Add and edit care tasks

3. Generate and view today's plan

- Briefly describe your initial UML design.


- What classes did you include, and what responsibilities did you assign to each?

I designed five classes:

- **`Task`** — represents one care activity, like a walk or feeding. Stores the name, how long it takes, and its priority.
- **`Pet`** — stores the pet's basic info and holds the list of tasks for that pet.
- **`Owner`** — stores the owner's name and how many minutes they have available each day.
- **`Scheduler`** — takes the owner and pet, picks which tasks fit in the available time, and returns a plan.
- **`DailyPlan`** — the result of scheduling. Keeps track of which tasks made the cut, which were skipped, and why.

**b. Design changes**

I made two small changes after reviewing the skeleton:

1. **Removed `__repr__` from `Task`.** I had added it as a stub, but since `Task` is a dataclass, Python already generates that method automatically. Keeping the stub would have broken it, so I removed it.

2. **Added `owner` to `DailyPlan`.** I realized the `explain()` method needed to know the owner's name and time budget to write a useful summary. Without it, `DailyPlan` had no way to access that information.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two constraints: time and priority. The owner's `available_minutes` acts as a hard cap — tasks that don't fit are skipped entirely. Within that budget, tasks are sorted so that `is_required=True` tasks always go first, followed by high, medium, and low priority tasks in that order.

I decided that time matters most because it's the one thing that can't be changed. Required tasks come next because they represent things like medication that have real consequences if skipped. Priority handles everything else, letting the scheduler favor important-but-optional tasks over nice-to-haves when time is tight.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The conflict detector only flags tasks that share the exact same `start_time` string (e.g., both at `"08:00"`). It does not check whether tasks *overlap* — for example, a 30-minute walk starting at `07:00` and a 10-minute feeding starting at `07:15` would not be flagged, even though they run at the same time.

This is a reasonable tradeoff for now because most pet care tasks happen one at a time and owners naturally assign distinct start times. Overlap detection would require comparing start times as integers and checking whether `start + duration > next_start`, which adds complexity without much benefit at this stage.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI across every phase: brainstorming the five classes and their responsibilities, generating the Mermaid UML diagram, writing method stubs, fleshing out the full implementation, connecting the backend to Streamlit, and adding the sorting, filtering, recurrence, and conflict detection algorithms.

The most useful prompts were specific and scoped to one task at a time. For example, "add a method to Scheduler that sorts tasks by start_time, with tasks that have no time set going last" produced clean and usable code. Open-ended prompts like "improve my scheduler" were less useful because they tended to suggest changes I had not asked for.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I asked AI to simplify `detect_conflicts()`, it suggested rewriting the warning loop as a single list comprehension. I adopted its suggestion to use `defaultdict(list)` from `collections`, which genuinely simplified the grouping logic. But I kept the explicit `for` loop for building the warning strings because the list comprehension version was harder to read and would have been harder to modify later. I verified the final version by running the conflict detection demo in `main.py` and confirming the expected warning appeared for the `08:00` collision.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested 5 behaviors: task completion status, task addition to a pet, chronological sorting by start time, daily recurrence creating the next occurrence, and conflict detection flagging a shared start time. These were important because they cover the core promise of the app — that tasks are tracked correctly, scheduled in order, repeated automatically, and flagged when they collide. If any of these broke silently, the daily plan would be wrong without the user knowing it.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident the scheduler handles the normal cases correctly — the tests all pass and the demo in `main.py` produces the expected output. My confidence drops for edge cases I have not tested yet: an owner with zero available minutes, a task whose `duration_minutes` exactly equals the remaining budget, weekly recurrence, and conflict detection when a task has no `start_time` set. I would write tests for those next.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part I am most satisfied with is the Scheduler class. It started as a simple greedy planner but grew to include sorting, filtering, recurrence, and conflict detection — all as separate, focused methods. Each method does one thing and can be called independently, which made testing straightforward and made it easy to wire each feature into the Streamlit UI without tangling logic together.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add true overlap detection to `detect_conflicts()` so it catches tasks that run at the same time even when their start times differ. I would also support multiple pets in the Streamlit UI — right now the app only manages one pet per session, but the backend already supports multiple pets through `Owner.pets`. Wiring that up in the UI would make the app match the full capability of the backend.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that AI is most useful when you already have a clear design. When I gave AI a specific task: "add this method with this signature", and it produced code I could use immediately. When I asked it to make broader decisions, I had to spend more time evaluating and trimming the output. Being the lead architect meant deciding what to build before asking AI to help build it, not the other way around.
