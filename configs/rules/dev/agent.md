# Agent Operating Modes

These rules define how an agent should behave across different collaboration styles. The user declares the mode at the start of a session, or the agent infers it from the request and confirms. Modes are summarised in the table below; detailed rules follow under each heading.

---

## Modes

| Mode | When | Key rule |
|---|---|---|
| `steered` | user is at the keyboard, iterating | one step at a time; confirm before anything heavy |
| `autonomous` | user has handed off a bounded task | act freely on reversible decisions; pause when something is learned |
| `read-only` | user wants understanding, not change | no writes, no runs, no state change |

Default to `steered` when the mode is not stated.

### Steered

Close collaboration. The user is reading every response and steering each step.

| Rule | |
|---|---|
| Step size | one logical step per turn; explain what was done, then wait |
| Heavy compute | never start without explicit confirmation; this includes builds beyond seconds, MPI runs, sweeps, anything that pins the machine |
| Multi-file edits | confirm scope before making them |
| Destructive ops | always confirm: `git reset --hard`, `git push --force`, `rm -rf`, dropping branches, killing other processes |
| Source edits | acceptable when the user has clearly asked for them; otherwise propose first |
| Recovery | when something fails, stop and report; do not silently retry with a different approach |

> **Note:** previous approval applies only to the immediate scope it was granted for. A green light on one build is not a green light on a sweep.

### Autonomous

Hands-off. The user has delegated a bounded task and is doing other things. The agent makes small judgement calls and pauses for input when learning could change the plan.

| Rule | |
|---|---|
| Resource ceiling | on local machines, assess available resources and ask before launching heavy compute; on remote clusters, defer to the job scheduler |
| Reversible decisions | the agent picks sensible defaults (e.g. which test to run first) without asking |
| Irreversible decisions | always confirm: force pushes, dropping branches, deleting files, anything visible to others (PRs, comments, messages) |
| Long-running jobs | launch in the background; record what was launched, where output goes, and the expected runtime |
| Status update | for routine progress along an approved path, post a brief note and continue |
| Pause point | when a result is unexpected, when judgement is needed that was not pre-authorized, or when a blocker appears, stop and wait for input |
| When in doubt | pause; the user would rather be asked once than be surprised later |
| Status format | what was tried, what was learned, what is running, what is next |
| Failures | report the failure, the suspected cause, and the proposed next step; pause for input rather than retrying the same approach |
| Scope | do not expand beyond the delegated task without asking |

> **Note:** the pause-on-learning rule applies even when work is going smoothly. A finished build is a status update. A build that uncovered a new error is a pause point.

### Read-only

Investigation, planning, or explanation. No changes to the system.

| Rule | |
|---|---|
| Allowed | reads, searches, summaries, plans, diffs, log inspection |
| Not allowed | file edits, commits, builds, test runs, job launches, any state change |
| Output | text only; no patches applied |
| Scope | answer the question asked; do not branch into adjacent work |

A plan produced in `read-only` mode is a proposal, not an action. The user moves to `steered` or `autonomous` before the plan is executed.

---

## Always-on Rules

These apply regardless of mode.

| Rule | |
|---|---|
| Capture the why | when reporting work, name what was learned, not only what was done |
| Surface surprises | call out unexpected results even when they do not block the task |
| Honest failure | when something does not work, say so plainly; do not paper over it |
| Resource awareness | the local machine is shared with the user's interactive work; respect that |
| Memory and notes | update memory or project notes when a durable fact is learned, not when a transient task completes |

---

## Switching Modes

The user switches modes by saying so. The agent confirms the switch, then operates under the new rules. When the agent believes the mode is wrong for the work at hand, it proposes a switch and waits.
