# Talk Types Reference

> **Scope**: Extends J.1 of design-principles.md, adds time allocation tables, content templates, best practices, and Q&A strategies for each talk type. Does NOT repeat the high-level talk type table from J.1.

---

## 1. Conference Talk (10–20 min)

Tight, focused, single-message. Audience is broad — assume mixed expertise. Every slide earns its place.

### Time Allocation (15-min version)

| Section | Time | Slides |
|---------|------|--------|
| Hook + problem statement | 2 min | 1–2 |
| Background / prior work | 2 min | 1–2 |
| Methods | 3 min | 2–3 |
| Results | 5 min | 3–4 |
| Conclusion + takeaway | 2 min | 1 |
| Buffer | 1 min | — |

### Time Allocation (10-min version)

| Section | Time | Slides |
|---------|------|--------|
| Hook + problem | 1.5 min | 1 |
| Background | 1 min | 1 |
| Methods | 2 min | 1–2 |
| Results | 4 min | 2–3 |
| Conclusion | 1.5 min | 1 |

### Content Template

```
Slide 1 — Hook: One sentence that makes the audience care.
  Example: "Every year, 10M people lose their homes to flooding — we can predict which ones."

Slide 2 — Problem: What gap does your work fill? One diagram, no equations.

Slides 3–4 — Methods: Enough to trust the results, not enough to reproduce them.
  One schematic > three paragraphs.

Slides 5–8 — Results: Lead with the punchline. Figure first, interpretation second.
  Each slide = one finding.

Slide 9 — Conclusion: Three bullets max. Restate the hook. What's next?
```

### Best Practices

- ✅ One message per slide
- ✅ Title = the finding ("AAI doubles under SSP5-8.5"), not the topic ("Results")
- ✅ Font ≥ 28pt for body text
- ✅ Backup slides for anticipated questions
- ✅ Practice with a timer — 15 min feels longer than it is
- ❌ No equations in main talk (move to backup)
- ❌ No "outline" slide for talks under 20 min
- ❌ No reading slides verbatim
- ❌ No more than 6 bullet points per slide

### Q&A Strategy

**Duration**: 5 min (built into session slot)

- Anticipate 2–3 questions: methodology, generalizability, next steps
- Prepare 2–3 backup slides: methods detail, sensitivity analysis, future work
- If question is out of scope: "Great question — outside this talk's scope, happy to discuss after"
- If you don't know: "I don't have that data — let me follow up with you"

---

## 2. Seminar / Invited Talk (45–60 min)

You're the expert. Audience expects depth, narrative arc, and intellectual generosity. Show the full story — including dead ends.

### Time Allocation (50-min version)

| Section | Time | Slides |
|---------|------|--------|
| Introduction + motivation | 8 min | 4–5 |
| Background + literature | 7 min | 4–6 |
| Methods (detailed) | 10 min | 5–8 |
| Results — main findings | 15 min | 8–10 |
| Discussion + implications | 7 min | 3–4 |
| Conclusion + future work | 3 min | 2 |

### Time Allocation (60-min version)

| Section | Time | Slides |
|---------|------|--------|
| Introduction + motivation | 10 min | 5–6 |
| Background + literature | 8 min | 5–7 |
| Methods (detailed) | 12 min | 6–10 |
| Results — main findings | 18 min | 10–14 |
| Discussion + implications | 8 min | 4–5 |
| Conclusion + future work | 4 min | 2–3 |

### Content Template

```
Opening (2 slides): Why does this problem matter? Broad → specific.
  Start with a real-world consequence, not a definition.

Background (4–6 slides): What did others do? Where did they fall short?
  Credit prior work generously. Show you know the field.

Methods (5–8 slides): Full workflow. Equations are OK here.
  One slide per major methodological choice. Justify each choice.

Results (8–12 slides): Multiple findings, each with its own slide.
  Include uncertainty. Show what didn't work and why.

Discussion (3–4 slides): What does this mean? What are the limits?
  Be honest about assumptions. Connect back to opening motivation.

Conclusion (2 slides): Summary + what's next. Acknowledge collaborators.
```

### Best Practices

- ✅ Use an outline slide — audience needs a map for 50+ min
- ✅ Revisit the outline after each major section ("We've covered X, now Y")
- ✅ Include a "what didn't work" slide — builds credibility
- ✅ Acknowledge collaborators early and specifically
- ✅ Leave 10 min for Q&A
- ❌ Don't rush the background — audience needs context
- ❌ Don't skip uncertainty quantification
- ❌ Don't end on a methods slide

### Q&A Strategy

**Duration**: 10–15 min

- Expect deep technical questions — prepare detailed backup slides
- Invite discussion: "I'd love to hear if others have seen this in different systems"
- For hostile questions: acknowledge the concern, state your assumption, offer to discuss after
- Write down questions you can't answer — follow up by email within 48h

---

## 3. Thesis Defense (30–45 min)

You know more about this than anyone in the room. Committee wants to see you can think, not just recite. Show ownership.

### Time Allocation (40-min version)

| Section | Time | Slides |
|---------|------|--------|
| Introduction + motivation | 5 min | 3–4 |
| Literature + gap | 5 min | 3–4 |
| Chapter 1 | 8 min | 5–7 |
| Chapter 2 | 8 min | 5–7 |
| Chapter 3 (if applicable) | 6 min | 4–5 |
| Synthesis + contributions | 5 min | 3 |
| Conclusion + future work | 3 min | 2 |

### Time Allocation (30-min version)

| Section | Time | Slides |
|---------|------|--------|
| Introduction + motivation | 4 min | 3 |
| Literature + gap | 3 min | 2–3 |
| Chapter 1 | 7 min | 4–5 |
| Chapter 2 | 7 min | 4–5 |
| Synthesis + contributions | 5 min | 3 |
| Conclusion | 4 min | 2 |

### Content Template

```
Introduction (3–4 slides): Frame the problem in the broadest context your work touches.
  End with: "This thesis addresses X by doing Y."

Literature (3–4 slides): Identify the gap. Show where your work sits.
  One slide: "What exists." One slide: "What's missing."

Per Chapter (5–7 slides each):
  - Research question for this chapter
  - Methods (brief — committee read the thesis)
  - Key result (one figure)
  - What this contributes

Synthesis (3 slides): How do the chapters connect?
  Show the through-line. This is the hardest slide to write — do it first.

Contributions (1 slide): Numbered list. "This thesis contributes: 1. … 2. … 3. …"

Future Work (1 slide): What would you do with 3 more years?
```

### Best Practices

- ✅ Prepare for questions on every methodological choice
- ✅ Have a "limitations" slide — committee will ask anyway
- ✅ Know your figures cold — be able to explain every axis
- ✅ Practice the full talk 3× with a timer
- ✅ Bring water
- ❌ Don't over-explain basics to the committee — they know
- ❌ Don't apologize for limitations — state them confidently
- ❌ Don't exceed your time — it signals poor preparation

### Q&A Strategy

**Duration**: 30–60 min (committee-driven)

- This is the real defense — the talk is preamble
- Expect: "Why did you choose X method over Y?"
- Prepare: alternative methods you considered and why you rejected them
- If you don't know: "That's outside the scope of this work, but here's how I'd approach it"
- For corrections: "You're right — I should have been clearer. What I meant was…"

---

## 4. Grant Pitch (10–20 min)

Reviewers are skeptical and busy. Lead with impact. Show feasibility. Make them believe you can do it.

### Time Allocation (15-min version)

| Section | Time | Slides |
|---------|------|--------|
| Problem + significance | 3 min | 2 |
| Gap + opportunity | 2 min | 1–2 |
| Proposed approach | 4 min | 3–4 |
| Preliminary results | 3 min | 2–3 |
| Team + timeline | 2 min | 1–2 |
| Budget overview | 1 min | 1 |

### Time Allocation (10-min version)

| Section | Time | Slides |
|---------|------|--------|
| Problem + significance | 2 min | 1–2 |
| Gap + approach | 3 min | 2–3 |
| Preliminary results | 3 min | 2 |
| Team + ask | 2 min | 1–2 |

### Content Template

```
Slide 1 — Significance: What problem? Who suffers? What's the cost of inaction?
  Use numbers: "2.4B people at risk" beats "many people affected."

Slide 2 — Gap: What's missing? Why hasn't this been solved?
  One sentence: "Current models can't X because Y."

Slides 3–5 — Approach: Specific aims. What will you do? How?
  Show a workflow diagram. Name the methods. Be concrete.

Slides 6–7 — Preliminary Data: Proof you can do this.
  One strong figure > three weak ones. Show it works at small scale.

Slide 8 — Team: Who's involved? Why are you the right team?
  Names + one-line credentials. Collaborators = credibility.

Slide 9 — Timeline + Budget: Gantt chart or milestone table.
  Budget: total ask + 2–3 major line items.
```

### Best Practices

- ✅ Lead with impact, not methods
- ✅ Preliminary data is non-negotiable — show proof of concept
- ✅ Name specific deliverables ("By month 18, we will have…")
- ✅ Show the team is complete — no obvious gaps
- ❌ Don't bury the ask — state it clearly
- ❌ Don't over-promise on timeline
- ❌ No jargon in the first two slides — reviewers may not be specialists

### Q&A Strategy

**Duration**: 5–10 min

- Expect: "What if X doesn't work?" → have a Plan B slide
- Expect: "Why you and not [competitor lab]?" → know the landscape
- Expect: "Is the budget realistic?" → know your numbers cold
- Close with: "We're confident this work will [specific outcome] — we'd welcome the opportunity to discuss further"

---

## 5. Journal Club (20–45 min)

You're presenting someone else's work. Your job: help the audience understand, evaluate, and critique it. Your opinion matters.

### Time Allocation (30-min version)

| Section | Time | Slides |
|---------|------|--------|
| Paper overview + context | 4 min | 2–3 |
| Research question + methods | 6 min | 3–4 |
| Key results | 8 min | 4–5 |
| Strengths + limitations | 6 min | 2–3 |
| Discussion questions | 6 min | 1–2 |

### Time Allocation (20-min version)

| Section | Time | Slides |
|---------|------|--------|
| Paper overview | 3 min | 2 |
| Methods | 4 min | 2–3 |
| Results | 7 min | 3–4 |
| Critique + questions | 6 min | 2 |

### Content Template

```
Slide 1 — Paper ID: Title, authors, journal, year. One-sentence summary.
  "This paper asks whether X causes Y, using Z dataset."

Slides 2–3 — Context: Why does this paper exist? What's the prior work?
  Your job: give the audience enough to evaluate the contribution.

Slides 4–6 — Methods: Reproduce the key methodological choices.
  Flag anything unusual or questionable.

Slides 7–10 — Results: Walk through the main figures.
  Reproduce the figures — don't just reference them.
  For each: "What does this show? Do you believe it?"

Slides 11–12 — Critique:
  Strengths: What did they do well?
  Limitations: What's missing? What would you do differently?
  Your verdict: Is this a significant contribution?

Slide 13 — Discussion Questions: 3 questions to drive conversation.
  Example: "They assume independence between sites — is that valid here?"
```

### Best Practices

- ✅ Read the paper 3× before building slides
- ✅ Check if results are reproducible (run the numbers if you can)
- ✅ Have an opinion — "I think this is weak because…"
- ✅ Prepare discussion questions in advance
- ❌ Don't just summarize — critique
- ❌ Don't skip the methods — that's where papers live or die
- ❌ Don't present figures you don't understand

### Q&A Strategy

**Duration**: 10–15 min (discussion-driven)

- Your role shifts to facilitator
- Use your prepared questions to seed discussion
- If discussion stalls: "What would you need to see to be convinced?"
- If someone disagrees with the paper: "Do others agree? What's the counter-argument?"

---

## 6. Lightning Talk (3–5 min)

One idea. One message. No exceptions. If you can't say it in 5 min, you don't understand it well enough yet.

### Time Allocation (5-min version)

| Section | Time | Slides |
|---------|------|--------|
| Hook + problem | 1 min | 1 |
| What you did | 1.5 min | 1–2 |
| Key result | 1.5 min | 1 |
| Call to action | 1 min | 1 |

### Time Allocation (3-min version)

| Section | Time | Slides |
|---------|------|--------|
| Hook + what you did | 1 min | 1 |
| Key result | 1.5 min | 1 |
| Call to action | 0.5 min | 1 |

### Content Template

```
Slide 1 — Hook: One sentence. Make them lean forward.
  "We can predict which buildings will flood — before the storm hits."

Slide 2 — What you did: Method in one sentence + one diagram.
  No details. Just enough to make the result credible.

Slide 3 — The result: One figure. The best one you have.
  Title = the finding. No explanation needed beyond the title.

Slide 4 — Call to action: What do you want from the audience?
  "Talk to me if you work with coastal exposure data."
  "The code is at github.com/yourname/repo."
  "We're looking for collaborators on the next phase."
```

### Best Practices

- ✅ Memorize the talk — no notes, no reading
- ✅ One slide per minute maximum
- ✅ Large fonts — 36pt minimum
- ✅ End with a specific ask
- ❌ No outline slide
- ❌ No equations
- ❌ No "and also…" — one message only
- ❌ Don't go over time — it's rude to the next speaker

### Q&A Strategy

**Duration**: 0–2 min (often none)

- Lightning talks rarely have formal Q&A
- End with: "Find me after the session if you want to dig in"
- Have a one-page handout or QR code to your paper/repo

---

## 7. Tutorial / Workshop (45–90 min)

Participants leave able to do something they couldn't before. Teaching, not presenting. Hands-on beats passive.

### Time Allocation (60-min version)

| Section | Time | Slides |
|---------|------|--------|
| Motivation + overview | 5 min | 3–4 |
| Concept block 1 + exercise | 15 min | 5–6 + exercise |
| Concept block 2 + exercise | 15 min | 5–6 + exercise |
| Concept block 3 + exercise | 15 min | 5–6 + exercise |
| Integration exercise | 7 min | 1–2 |
| Wrap-up + resources | 3 min | 2 |

### Time Allocation (90-min version)

| Section | Time | Slides |
|---------|------|--------|
| Motivation + overview | 8 min | 4–5 |
| Concept block 1 + exercise | 20 min | 6–8 + exercise |
| Concept block 2 + exercise | 20 min | 6–8 + exercise |
| Concept block 3 + exercise | 20 min | 6–8 + exercise |
| Integration exercise | 15 min | 2–3 |
| Wrap-up + resources | 7 min | 3 |

### Content Template

```
Opening (3–4 slides):
  - What will participants be able to do by the end?
  - Prerequisites: what do they need to know?
  - Setup: is everything installed? (Check before you start.)

Per Concept Block (5–8 slides + exercise):
  - Concept slide: What is it? Why does it matter?
  - Example slide: Show it working on a real case
  - Code/demo slide: Live or screenshot
  - Exercise: Participants do it themselves (5–8 min)
  - Solution reveal: Walk through the answer

Integration Exercise (2–3 slides):
  - Combine concepts from all blocks
  - Real dataset, real problem
  - Participants work in pairs

Wrap-up (2–3 slides):
  - What did we cover? (Checklist format)
  - Where to go next? (3–5 specific resources)
  - How to get help? (GitHub issues, Slack, email)
```

### Best Practices

- ✅ Test all code/demos the day before on the same OS participants use
- ✅ Have a fallback for participants who can't install software (cloud notebook)
- ✅ Build in buffer — exercises always take longer than expected
- ✅ Circulate during exercises — don't stand at the front
- ✅ Provide all materials in advance (repo, notebook, data)
- ❌ Don't lecture for more than 15 min without an exercise
- ❌ Don't use live internet demos — they fail
- ❌ Don't assume everyone has the same setup
- ❌ Don't skip the wrap-up — participants need closure

### Q&A Strategy

**Duration**: Ongoing throughout + 5–10 min at end

- Encourage questions during exercises, not during lecture
- For questions that derail: "Great — let's put that in the parking lot and come back"
- Maintain a visible "parking lot" (whiteboard or shared doc) for deferred questions
- End with: "Everything in the parking lot — let's address these now or async"
- Send a follow-up email with answers to parking lot questions within 24h
