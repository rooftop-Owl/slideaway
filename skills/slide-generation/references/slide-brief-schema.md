# Slide Brief Schema

> **Scope**: This schema defines the contract between the planning agent (slide-coach) and all downstream pipeline stages (slide-creator, content-reviewer, design-reviewer). The Slide Brief is the single structured artifact that flows through the entire pipeline. Every field documented here is either required or explicitly optional. Downstream agents consume the brief — they do not modify it.

---

## Schema Version

`slide-brief/1.0`

All briefs MUST include a `schema_version` field set to this value. Pipeline agents MUST reject briefs with unknown schema versions.

---

## Field Reference

### 1. Audience

Who you're talking to determines everything else.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audience.current_state` | string | **yes** | What the audience believes or knows right now. One sentence. |
| `audience.desired_state` | string | **yes** | What the audience should believe or know after the talk. One sentence. |
| `audience.quadrant` | enum | **yes** | One of: `deep-insider`, `deep-outsider`, `shallow-insider`, `shallow-outsider` |
| `audience.attention_budget` | enum | **yes** | One of: `high` (captive, invested), `medium` (willing but distracted), `low` (skeptical or forced) |

**Quadrant definitions:**

| Quadrant | Domain Knowledge | Familiarity with Your Work | Implication |
|----------|-----------------|---------------------------|-------------|
| `deep-insider` | Expert | Knows your project | Skip background. Go deep on results. |
| `deep-outsider` | Expert in adjacent field | Doesn't know your work | Bridge from their domain. Motivate why your problem matters. |
| `shallow-insider` | Non-expert | Knows your project exists | Explain methods simply. Emphasize impact. |
| `shallow-outsider` | Non-expert | No prior exposure | Start from scratch. Lead with story. Minimize jargon. |

**Attention budget guidance:**

- `high` — Conference keynote, thesis defense, invited seminar. They chose to be here.
- `medium` — Regular conference session, team meeting, journal club. Competing with phones.
- `low` — Mandatory training, large lecture, pitch to skeptical stakeholders. Earn every minute.

---

### 2. Purpose

What the talk exists to accomplish.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `purpose.the_one_thing` | string | **yes** | Single sentence the audience must remember. If they forget everything else, this survives. |
| `purpose.the_ask` | enum | **yes** | What the audience should DO after: `fund`, `adopt`, `approve`, `collaborate`, `understand`, `implement`, `teach`, `decide`, `none` |
| `purpose.talk_type` | enum | **yes** | One of: `conference`, `seminar`, `defense`, `pitch`, `journal-club`, `lightning`, `tutorial`, `internal`, `workshop` |

**Talk type quick reference:**

| Type | Typical Duration | Audience Expectation | Key Constraint |
|------|-----------------|---------------------|----------------|
| `conference` | 10–20 min | Breadth audience, single message | Ruthless focus — one finding per slide |
| `seminar` | 45–60 min | Depth audience, full narrative | Show the journey, including dead ends |
| `defense` | 20–45 min (presentation) | Committee, prove competence | Anticipate challenges, backup slides mandatory |
| `pitch` | 5–15 min | Decision-makers, ROI focus | Lead with outcome, not process |
| `journal-club` | 15–30 min | Peers, critical analysis | Evaluate someone else's work, not yours |
| `lightning` | 3–5 min | Mixed, high energy | One idea. No warmup. Punch immediately. |
| `tutorial` | 60–120 min | Learners, hands-on | Interleave theory with exercises |
| `internal` | 15–45 min | Team/org, status or retrospective | Be direct. Skip the sales pitch. |
| `workshop` | 90–240 min | Participants, collaborative | Breakout activities, flexible pacing |

---

### 3. Structure

How the talk is organized in time and narrative.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `structure.duration_minutes` | integer | **yes** | Total talk time in minutes, excluding Q&A |
| `structure.slide_count_target` | integer | **yes** | Target number of content slides (not counting title/backup) |
| `structure.narrative_arc` | enum | **yes** | One of: `hourglass`, `scr`, `pyramid`, `assertion-evidence`, `problem-solution`, `journey` |
| `structure.time_blocks` | array | **yes** | Ordered list of `{section, minutes, slide_range}` objects |

**Narrative arc definitions:**

| Arc | Shape | Best For | Structure |
|-----|-------|----------|-----------|
| `hourglass` | Broad → narrow → broad | Conference talks, seminars | Context → Focus → Implications |
| `scr` | Linear | Problem-driven talks, pitches | Situation → Complication → Resolution |
| `pyramid` | Bottom-up | Data-heavy, evidence-first | Evidence → Analysis → Conclusion |
| `assertion-evidence` | Claim-first | Technical, assertion per slide | Assertion title + supporting visual |
| `problem-solution` | Two-act | Pitches, proposals | Problem (pain) → Solution (relief) |
| `journey` | Chronological | Seminars, defenses | Timeline of discovery, including failures |

**Time blocks example:**

```yaml
time_blocks:
  - section: "Hook + problem"
    minutes: 2
    slide_range: [1, 2]
  - section: "Methods"
    minutes: 3
    slide_range: [3, 5]
  - section: "Results"
    minutes: 5
    slide_range: [6, 9]
  - section: "Conclusion"
    minutes: 2
    slide_range: [10, 10]
  - section: "Buffer"
    minutes: 1
    slide_range: null
```

---

### 4. Style

Visual identity and rendering engine.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `style.preset` | string | **yes** | Named style from the 30-preset catalog (e.g., `executive-suite`, `research-clean`, `dark-terminal`) |
| `style.engine` | enum | **yes** | One of: `marp`, `md2pptx`, `pptx`, `revealjs`, `beamer`, `html`, `rise` |
| `style.template` | string | no | Path to a `.pptx` or `.tex` template file. Overrides preset defaults when provided. |
| `style.anti_slop_verified` | boolean | **yes** | Coach confirms the preset passes anti-slop checks (no banned fonts, no banned colors, no generic layouts). Must be `true`. |

**Anti-slop rule**: If `anti_slop_verified` is `false` or missing, the pipeline MUST reject the brief. No exceptions. The coach is responsible for verifying this before emitting the brief.

---

### 5. Constraints (Optional)

Situational requirements that override defaults.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `constraints.brand` | object | no | `{logo_path, primary_color, secondary_color, font_family}` — corporate identity overrides |
| `constraints.accessibility` | object | no | `{min_font_size, contrast_ratio, colorblind_safe}` — WCAG or venue requirements |
| `constraints.language` | string | no | ISO 639-1 code (e.g., `en`, `ko`, `de`). Defaults to `en`. |
| `constraints.required_sections` | array | no | List of section names that MUST appear (e.g., `["Acknowledgments", "References"]`) |
| `constraints.source_material` | array | no | List of `{path, type, description}` objects pointing to input files (papers, notes, data) |
| `constraints.max_file_size_kb` | integer | no | Maximum output file size. Relevant for email-attached decks. |
| `constraints.output_formats` | array | no | List of required output formats: `["pptx", "pdf"]`. Defaults to engine native format. |

---

## Validation Rules

Pipeline agents enforce these rules before processing a brief.

### Hard Failures (reject the brief)

1. **Missing required field** — Any field marked `required: yes` above is absent or null → reject with error naming the missing field.
2. **Invalid enum value** — A field contains a value not in its enum set → reject with error showing valid options.
3. **Schema version mismatch** — `schema_version` is missing or not `slide-brief/1.0` → reject.
4. **Anti-slop not verified** — `style.anti_slop_verified` is `false` or missing → reject.
5. **Time blocks don't sum** — Sum of `time_blocks[].minutes` differs from `structure.duration_minutes` by more than 1 minute → reject.
6. **Slide range exceeds target** — Max slide number in `time_blocks` exceeds `structure.slide_count_target` + 2 (title + buffer) → reject.

### Warnings (proceed with caution)

1. **Attention budget mismatch** — `audience.attention_budget` is `low` but `structure.duration_minutes` > 30 → warn: "Low-attention audience + long talk. Consider cutting."
2. **Lightning without punch** — `purpose.talk_type` is `lightning` but `structure.duration_minutes` > 5 → warn: "Lightning talks are ≤5 min."
3. **No source material for tutorial** — `purpose.talk_type` is `tutorial` but `constraints.source_material` is empty → warn: "Tutorials usually need reference material."

---

## Consumer Rules

**Downstream agents MUST quote which brief fields they reference when making decisions.**

This is non-negotiable. Every design choice, content decision, or structural judgment in the pipeline must trace back to a specific brief field. Examples:

### slide-creator (Content Generation)

```
Per brief.structure.narrative_arc = "scr", structuring as:
  Situation (slides 1–3) → Complication (slides 4–5) → Resolution (slides 6–9)

Per brief.audience.quadrant = "deep-outsider", including a 2-slide domain bridge
before diving into methods.

Per brief.purpose.the_one_thing = "Coastal flood risk doubles by 2050 under SSP5-8.5",
placing this as the title slide subtitle AND the final slide takeaway.
```

### content-reviewer (Content QA)

```
Checking brief.purpose.the_one_thing appears on at least 2 slides (title + conclusion).
FAIL: "The One Thing" not found on conclusion slide.

Checking brief.structure.time_blocks against actual slide count per section.
WARN: Results section has 6 slides but brief allocates 4. Presenter will rush.
```

### design-reviewer (Visual QA)

```
Per brief.style.preset = "research-clean", verifying:
  - Font family matches preset spec
  - Color palette within preset bounds
  - No banned fonts or colors (brief.style.anti_slop_verified = true)

Per brief.constraints.accessibility.min_font_size = 24,
flagging slide 7 body text at 18pt. FAIL.
```

**Why this matters**: When a reviewer flags an issue, the creator can trace it back to the brief. When the coach revises the brief, every downstream agent knows exactly which of their decisions are affected. No ambiguity. No "I assumed."

---

## Example Briefs

### Example 1: Conference Talk

```yaml
schema_version: "slide-brief/1.0"

audience:
  current_state: "Knows climate risk modeling exists but hasn't used CLIMADA"
  desired_state: "Understands that CLIMADA can quantify coastal flood risk at municipality level"
  quadrant: "deep-outsider"
  attention_budget: "medium"

purpose:
  the_one_thing: "CLIMADA resolves flood risk to individual municipalities, enabling targeted adaptation spending"
  the_ask: "adopt"
  talk_type: "conference"

structure:
  duration_minutes: 15
  slide_count_target: 10
  narrative_arc: "hourglass"
  time_blocks:
    - section: "Hook — global flood losses"
      minutes: 2
      slide_range: [1, 2]
    - section: "CLIMADA methodology"
      minutes: 3
      slide_range: [3, 4]
    - section: "Philippines case study results"
      minutes: 5
      slide_range: [5, 8]
    - section: "Implications for adaptation policy"
      minutes: 3
      slide_range: [9, 10]
    - section: "Buffer"
      minutes: 2
      slide_range: null

style:
  preset: "research-clean"
  engine: "marp"
  anti_slop_verified: true

constraints:
  language: "en"
  required_sections: ["Acknowledgments"]
  source_material:
    - path: "paper_draft_v3.pdf"
      type: "manuscript"
      description: "Submitted paper with all figures and tables"
    - path: "data/philippines_results.csv"
      type: "data"
      description: "Municipality-level AAI results"
```

### Example 2: PhD Defense

```yaml
schema_version: "slide-brief/1.0"

audience:
  current_state: "Committee has read the thesis but needs a coherent oral narrative"
  desired_state: "Convinced the candidate demonstrated independent research capability and novel contribution"
  quadrant: "deep-insider"
  attention_budget: "high"

purpose:
  the_one_thing: "This thesis introduces a validated framework for compound flood-drought risk assessment under climate change"
  the_ask: "approve"
  talk_type: "defense"

structure:
  duration_minutes: 35
  slide_count_target: 28
  narrative_arc: "journey"
  time_blocks:
    - section: "Motivation and research questions"
      minutes: 5
      slide_range: [1, 4]
    - section: "Chapter 1 — Historical compound events"
      minutes: 8
      slide_range: [5, 10]
    - section: "Chapter 2 — Framework development"
      minutes: 8
      slide_range: [11, 16]
    - section: "Chapter 3 — Future projections"
      minutes: 8
      slide_range: [17, 22]
    - section: "Synthesis and contributions"
      minutes: 4
      slide_range: [23, 26]
    - section: "Outlook and open questions"
      minutes: 2
      slide_range: [27, 28]

style:
  preset: "academic-formal"
  engine: "beamer"
  template: "templates/beamer/defense.tex"
  anti_slop_verified: true

constraints:
  accessibility:
    min_font_size: 22
    contrast_ratio: 4.5
    colorblind_safe: true
  required_sections: ["Research Questions", "Contributions", "References"]
  source_material:
    - path: "thesis_final.pdf"
      type: "thesis"
      description: "Complete thesis document"
    - path: "figures/"
      type: "directory"
      description: "Publication-quality figures from all three chapters"
```

### Example 3: Internal Team Retrospective

```yaml
schema_version: "slide-brief/1.0"

audience:
  current_state: "Team lived through Q1 but hasn't reflected on patterns"
  desired_state: "Aligned on 3 process changes for Q2"
  quadrant: "shallow-insider"
  attention_budget: "low"

purpose:
  the_one_thing: "We shipped 40% more but our review bottleneck ate the gains — fix reviews, fix velocity"
  the_ask: "decide"
  talk_type: "internal"

structure:
  duration_minutes: 20
  slide_count_target: 12
  narrative_arc: "problem-solution"
  time_blocks:
    - section: "Q1 by the numbers"
      minutes: 3
      slide_range: [1, 3]
    - section: "What went well"
      minutes: 4
      slide_range: [4, 6]
    - section: "The review bottleneck"
      minutes: 5
      slide_range: [7, 9]
    - section: "Three proposals for Q2"
      minutes: 5
      slide_range: [10, 12]
    - section: "Buffer for discussion"
      minutes: 3
      slide_range: null

style:
  preset: "minimalist"
  engine: "marp"
  anti_slop_verified: true

constraints:
  language: "en"
  required_sections: ["Action Items"]
```

---

## Brief Lifecycle

```
slide-coach (producer)
    │
    ├─ Gathers user input (topic, audience, constraints)
    ├─ Fills all required fields
    ├─ Runs anti-slop verification
    ├─ Validates against this schema
    ├─ Emits the brief
    │
    ▼
slide-creator (consumer)
    │
    ├─ Reads brief, quotes fields for every decision
    ├─ Generates slides per structure.time_blocks
    ├─ Applies style.preset + style.engine
    │
    ▼
content-reviewer (consumer)
    │
    ├─ Checks slides against brief.purpose and brief.audience
    ├─ Verifies the_one_thing appears prominently
    ├─ Validates section timing against time_blocks
    │
    ▼
design-reviewer (consumer)
    │
    ├─ Checks visual compliance against brief.style
    ├─ Enforces brief.constraints.accessibility
    ├─ Runs anti-slop checks independently
    │
    ▼
Final output (validated deck)
```

No agent in the pipeline modifies the brief. If the brief needs revision, control returns to the coach. The brief is immutable once emitted.
