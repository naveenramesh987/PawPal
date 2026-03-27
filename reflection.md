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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
