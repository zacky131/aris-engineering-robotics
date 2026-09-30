# Story Spine — Global Rule

All research outputs must maintain a coherent story structure.

## Core story spine

```
Problem
  └─ What real challenge motivates this work?
Gap
  └─ What does existing work not solve? What is the specific missing piece?
Insight
  └─ What is the key intellectual contribution or observation that enables progress?
Method
  └─ What did you design, build, or derive?
Evidence
  └─ What experiments did you run? What metrics did you obtain?
Boundary
  └─ What does the evidence NOT show? What are the scope limits?
Implication
  └─ What does this result mean for researchers or practitioners within the stated scope?
```

## Robotics research extensions

For robotics papers, explicitly address:

| Element | Robotics-specific questions |
|---|---|
| Problem | Which platform? Which operating environment? Which task? |
| Gap | Which baseline does the proposed method outperform? Why is that baseline insufficient? |
| Method | What is the system architecture? What assumptions does the controller/estimator make? |
| Evidence | Which evidence level (L0–L6)? How many trials? Which scenarios? |
| Boundary | Is this SIL only? One robot? One weather condition? One scenario type? |
| Implication | For which real system or application is this result relevant, within these boundaries? |

## Anti-patterns to avoid

- Jumping from method to claim without evidence
- Omitting boundary statements (scope inflation)
- Mentioning deployment without L5/L6 evidence
- Treating a simulation result as proof of real-world performance

---

Source: adapted from `engineering-paper-skills/skills/_shared/story-spine.md`
Extended with robotics evidence level and scope elements.
