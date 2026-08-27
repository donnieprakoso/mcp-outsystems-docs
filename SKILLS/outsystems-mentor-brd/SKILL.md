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
- Mentor App Generator capabilities and limitations (ODC)
- Common app architecture patterns in ODC
- Best practices for app decomposition and modularity
- Integration patterns and connectors

Run searches in parallel. See `./system-prompt.md` for specific queries.

### Step 3: Analyze for Single vs. Multi-App

Based on interview answers + Mentor capabilities, determine:
- Is this best served by **one focused app**, or **multiple coordinated apps**?
- If multi-app: what are the natural boundaries (by domain, responsibility, team)?
- What are the integration points?

If multi-app is detected, generate a proposed app breakdown and present it to the user: *"Based on your requirements, I'm seeing [X] distinct app boundaries. Does this make sense, or would you adjust it?"*

### Step 4: Generate BRD(s)

**Single app:**
- Generate one BRD using the template in `./system-prompt.md`
- Filename: `BRD-[AppName]-[Date].md`

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

### BRD Structure (all files)

Every BRD follows this structure (see `./system-prompt.md` for detailed template):

```
# Business Requirements Document: [App Name]

> **For:** Mentor App Generator (ODC)
> **Generated:** [Date]
> **Research basis:** OutSystems Mentor documentation (synced [date from MCP])

## Executive Summary
[1–2 paragraphs: what problem this app solves, for whom, why it matters]

## App Scope & Boundaries
[What this app does, what it explicitly does NOT do]
[If part of a multi-app system, reference parent architecture doc]

## Functional Requirements
[Key workflows, user interactions, features]

## Non-Functional Requirements
[Performance, scale, security, compliance, integration constraints]

## Data & Integration
[Key entities, external systems, APIs, data flows]

## Acceptance Criteria
[How the user will know this app is successful]

## Dependencies & Risks
[Other apps, external systems, technical risks, mitigation]

## Success Metrics
[KPIs, business outcomes, launch readiness criteria]
```

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
- **Grounding:** Every BRD section is informed by actual Mentor capabilities found via MCP research, not generic requirements templates
- **Length:** 
  - Single app BRD: 800–1200 words
  - Multi-app architecture doc: 500–700 words
  - Individual app BRDs in multi-app: 600–1000 words each
- **Mentor readiness:** All output is formatted for direct upload to Mentor App Generator
- **Freshness:** Every BRD includes the date of the Mentor documentation research (from MCP `last_updated()`)
- **No assumptions:** If MCP search returns nothing on a topic, say so rather than inventing guidance

---

## Anti-Patterns

Do NOT:
- Create a BRD that ignores Mentor's actual capabilities (research first)
- Generate multiple BRDs without a coordinating architecture document
- Use generic BRD templates that don't reflect Mentor's strengths
- Skip the interview — assume you know what the user needs
- Name apps arbitrarily — use clear, domain-driven names (e.g., `PaymentProcessor`, not `App1`)

---

## When NOT to Use This Skill

- If the user's goal is to build ON TOP OF an existing Mentor-generated app (use a different skill for app enhancement)
- If they're designing a system for a platform other than ODC (this skill is ODC-only)
- If they want a generic BRD template with no Mentor guidance (they don't need this skill)
