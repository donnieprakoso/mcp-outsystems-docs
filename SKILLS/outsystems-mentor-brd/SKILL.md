---
name: outsystems-mentor-brd
description: >
  Use this skill when you need to create a Business Requirements Document (BRD) for building with OutSystems Mentor App Generator on ODC. Triggers on phrases like 'create a BRD for Mentor', 'generate a BRD for my Mentor app', 'I want to use Mentor to build this', 'help me structure requirements for Mentor', or any request to prepare a document for Mentor App Generator upload. The skill conducts an interactive interview to understand requirements, searches OutSystems documentation for Mentor best practices, and generates either a single BRD or multiple coordinated BRDs (if the requirements indicate a multi-app architecture). Single-document output is ready to upload directly to Mentor.
---

# OutSystems Mentor App Generator BRD Builder

## What This Skill Does

Transforms a user's requirements (or a blank slate) into one or more **Mentor-ready BRD documents**, grounded in ODC best practices and Mentor App Generator capabilities. The skill identifies whether the requirements point to a single app or multiple coordinated apps, and generates appropriately:

- **Single app:** One focused BRD file
- **Multiple apps:** Parent architecture document + individual BRDs per app, with dependency mapping

All output is optimized for direct upload to Mentor App Generator and structured around Mentor's actual capabilities.

---

## Inputs

The user provides either:
1. **A problem statement or existing document** — describing what they want to build
2. **No input** — skill conducts a discovery interview from scratch
3. **A partial outline or notes** — skill clarifies and enriches via interview

---

## Procedure

### Step 1: Conduct Interactive Interview

Start by understanding the user's requirements. Ask clarifying questions covering:
- **Problem & goals** — what are they solving, for whom, why now?
- **Scope & scale** — number of users, data volume, performance needs?
- **Key workflows** — what are the main processes/interactions?
- **Integrations** — what systems does this need to connect to?
- **Constraints** — regulatory, performance, timeline, team size?

Ask questions one at a time, listen to answers, and adapt follow-ups based on responses. See `./system-prompt.md` for the full interview template.

After 5–7 key questions, pause and summarize: *"Based on what you've told me, I'm seeing [summary]. Does that match your vision?"*

### Step 2: Search Mentor Docs & Best Practices

Search the OutSystems documentation MCP (`outsystems-docs`) for:
- The current Mentor requirement-document structure, data types, UI pattern vocabulary, and dashboard capabilities — run this **every session**, even though `./Mentor-Requirement-Doc-Standards.md` caches a snapshot of it, because Mentor Web ships new capabilities frequently and the cache can drift from what's live
- Mentor App Generator capabilities and limitations (ODC)
- Common app architecture patterns in ODC
- Best practices for app decomposition and modularity
- Integration patterns and connectors

Run searches in parallel. Compare `last_updated()` against the date noted in `./Mentor-Requirement-Doc-Standards.md`; if MCP is newer, pull the full docs and use them over the cached file. See `./system-prompt.md` for specific queries.

### Step 3: Analyze for Single vs. Multi-App

Based on interview answers + Mentor capabilities, determine:
- Is this best served by **one focused app**, or **multiple coordinated apps**?
- If multi-app: what are the natural boundaries (by domain, responsibility, team)?
- What are the integration points?

If multi-app is detected, generate a proposed app breakdown and present it to the user: *"Based on your requirements, I'm seeing [X] distinct app boundaries. Does this make sense, or would you adjust it?"*

### Step 4: Generate BRD(s)

Before drafting, open the `./resources/` sample closest to the app's domain and pattern-match your draft against it directly (section headers, entity block formatting, role/permission phrasing) — it's OutSystems' own official example of what Mentor accepts, not just background reading. See `./system-prompt.md` Part 3.5.

**Single app:**
- Generate **two files** using the templates in `./system-prompt.md`:
  - `BRD-[AppName]-[Date].md` — Mentor-native structure only, ready for direct upload to Mentor App Generator
  - `BRD-[AppName]-Context-[Date].md` — stakeholder-facing background (executive summary, non-functional requirements, risks, KPIs); never uploaded to Mentor

**Multiple apps:**
- Generate parent architecture document: `00-BRD-Architecture-[ProjectName]-[Date].md`
  - System overview, app boundaries, integration points, dependencies
- Generate individual BRDs: `01-BRD-[AppName1]-[Date].md`, `02-BRD-[AppName2]-[Date].md`, etc.
  - Each BRD is self-contained but references the parent architecture doc
  - Each identifies its dependencies on other apps (from the parent doc)

### Step 5: Output & Present

Save all files to the current working directory. Present them to the user with a summary:
- What the BRD(s) cover
- Recommended next steps (upload to Mentor, review with stakeholders, refine requirements)
- Any gaps or assumptions surfaced during research

---

## Output Format

### The Mentor-Upload File (per app — this is what goes into Mentor App Generator)

Follows Mentor's own native document structure, not a generic BRD shape — see `./Mentor-Requirement-Doc-Standards.md` for the full vocabulary (canonical data types, entity syntax, role/permission levels, UI pattern keywords, dashboard chart/aggregation vocabulary) and `./system-prompt.md` for the detailed template:

```
# [App Name] — Requirement Document

> **For:** Mentor App Generator (ODC)
> **Generated:** [Date]
> **Research basis:** OutSystems Mentor documentation (synced [date from MCP])

## App Overview
[1–2 paragraphs: purpose, key users, why it matters]

## General App Settings
[Optional: theme, dark mode, primary color]

## Data Model
[Entities as lists, not tables — exact "Entity: X / stored locally.../ Attributes include: - Name: DataType, description" syntax]
[Static entities with Purpose + Records]

## Roles and Permissions
[Per role: entity → View/Edit/No Access, with row-level scoping named explicitly]

## Main Features and Screens
[Screens with recognized UI pattern keywords; dashboard specs with real chart types + aggregations]

## External Integrations
[Optional: named Data Fabric connections, with the "must exist in ODC before generation" prerequisite flagged]
```

Written entirely as lists, not tables — Mentor parses structured lists far more reliably, and this is explicit official guidance.

### The Context Companion File (per app — NOT uploaded to Mentor)

Holds everything a generic BRD would have but Mentor doesn't need: Executive Summary, Non-Functional Requirements, Acceptance Criteria, Dependencies & Risks (tables are fine here), Success Metrics & KPIs. Given to stakeholders for sign-off; kept separate so the Mentor-upload file stays lean and parseable.

### Multi-App Architecture Document

If multiple apps are identified, the parent document (`00-BRD-Architecture-...md`) includes:

```
# System Architecture & BRD Overview: [Project Name]

## System Vision
[What the overall system accomplishes, for whom]

## App Breakdown
[Table: App Name | Responsibility | Key Integrations | Owner]

## Integration Map
[Diagram or flowchart showing app boundaries and data flows]

## Cross-App Dependencies
[What each app needs from others, timing/sequencing notes]

## Success Criteria (System-Level)
[End-to-end business outcomes]

## Recommended Build Order
[Which apps to build first, sequencing rationale]

### Individual BRDs
- See `01-BRD-[AppName1].md`, `02-BRD-[AppName2].md`, etc.
```

---

## Output Standards

- **Tone:** Business-focused, not technical jargon (but specific about Mentor/ODC capabilities)
- **Grounding:** Every BRD section is informed by actual Mentor capabilities found via MCP research, not generic requirements templates or a stale cached snapshot — re-query `outsystems-docs` every session (see `./system-prompt.md` Part 2)
- **Length:** 
  - Single app BRD (Mentor-upload file): 400–700 words
  - Single app context companion: 400–800 words
  - Multi-app architecture doc: 500–700 words
  - Individual app BRDs in multi-app: 400–700 words each
- **Mentor readiness:** The Mentor-upload file follows Mentor's own native document structure (`./Mentor-Requirement-Doc-Standards.md`) — canonical data types, list-based entity/role/screen syntax, no tables, no PII, no ambiguous language — and is formatted for direct upload
- **Freshness:** Every file includes the date of the Mentor documentation research (from MCP `last_updated()`); flag to the user if that date is materially behind what the live docs show
- **No assumptions:** If MCP search returns nothing on a topic, say so rather than inventing guidance

---

## Anti-Patterns

Do NOT:
- Create a BRD that ignores Mentor's actual capabilities (research first)
- Generate multiple BRDs without a coordinating architecture document
- Use generic BRD templates that don't reflect Mentor's strengths
- Skip the interview — assume you know what the user needs
- Name apps arbitrarily — use clear, domain-driven names (e.g., `PaymentProcessor`, not `App1`)
- Put stakeholder-narrative content (executive summary, risk register, KPI tables, acceptance-criteria checklists) into the Mentor-upload file — that belongs in the `-Context-` companion file
- Use markdown tables, invented data types, PII, implementation code, or ambiguous language ("user-friendly", "intuitive") in the Mentor-upload file
- Trust `./Mentor-Requirement-Doc-Standards.md` as the final word — always re-verify against live MCP research first

---

## When NOT to Use This Skill

- If the user's goal is to build ON TOP OF an existing Mentor-generated app (use a different skill for app enhancement)
- If they're designing a system for a platform other than ODC (this skill is ODC-only)
- If they want a generic BRD template with no Mentor guidance (they don't need this skill)
