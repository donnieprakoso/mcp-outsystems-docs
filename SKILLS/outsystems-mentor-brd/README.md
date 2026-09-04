# OutSystems Mentor BRD Builder Skill

## Overview

This skill generates Business Requirements Documents (BRDs) for building with OutSystems Mentor App Generator on ODC.

### What makes it different

- **Interactive interview** — asks clarifying questions instead of assuming requirements
- **Multi-app aware** — automatically detects if your requirements need multiple coordinated apps
- **Mentor-grounded, live** — researches actual Mentor capabilities and document standards via OutSystems Docs MCP *every session*, not just a cached template. `Mentor-Requirement-Doc-Standards.md` caches a snapshot for speed, but the skill re-verifies it against the MCP each run since Mentor Web ships new capabilities frequently
- **Ready to upload** — the Mentor-facing file follows Mentor's own native document structure (canonical data types, list-based entity/role/screen syntax, no tables) so it uploads cleanly into Mentor App Generator

### Single vs. Multi-App

- **Single app**: Generates one focused BRD
- **Multiple apps**: Generates parent architecture document + individual BRDs per app, with dependency mapping

---

## How to Use

Invoke the skill and say something like:

- "Create a BRD for my Mentor app"
- "Generate a BRD using Mentor App Generator"
- "I want to build this with Mentor — help me create requirements"
- "Create a proper BRD for my Mentor project"

The skill will:
1. Interview you about your requirements
2. Search OutSystems Docs for Mentor best practices
3. Identify if you need one app or multiple coordinated apps
4. Generate the appropriate BRDs
5. Output files ready to upload to Mentor

---

## Output Files

### Single App

```
BRD-[AppName]-[YYYY-MM-DD].md          ← Upload this to Mentor App Generator
BRD-[AppName]-Context-[YYYY-MM-DD].md  ← Stakeholder background, not for Mentor
```

The first file follows Mentor's own native document structure — App Overview, General App Settings, Data Model, Static Entities, Roles & Permissions, Main Features & Screens, External Integrations — written as lists, not tables, so Mentor parses it reliably. The second file carries the executive summary, non-functional requirements, risks, and KPIs that stakeholders need but Mentor doesn't.

### Multiple Apps

```
00-BRD-Architecture-[ProjectName]-[YYYY-MM-DD].md  ← Start here (planning doc, not for Mentor)
01-BRD-[AppName1]-[YYYY-MM-DD].md                  ← Upload to Mentor
02-BRD-[AppName2]-[YYYY-MM-DD].md                  ← Upload to Mentor
...
```

- **Architecture doc** shows app boundaries, dependencies, integration map, risk register, and build sequencing — a human-facing planning artifact, never uploaded to Mentor
- **Individual BRDs** are Mentor-native and self-contained, ready for direct upload

---

## Key Features

### Interview Phase
Asks about:
- Problem & vision
- User scope & scale
- Key workflows
- Integrations
- Constraints & compliance

### Research Phase
Searches Mentor docs for:
- Mentor's current requirement-document structure, canonical data types, UI pattern vocabulary, and dashboard capabilities — run live every session, since Mentor Web ships new capabilities frequently and the cached reference (`Mentor-Requirement-Doc-Standards.md`) can drift from what's actually live
- Mentor capabilities and limitations
- Multi-app architecture patterns in ODC
- Integration best practices
- Security and compliance guidance

### Analysis Phase
Determines:
- Single or multi-app architecture
- Clear app boundaries (if multi-app)
- Dependencies and sequencing

### Generation Phase
Creates, per app, a Mentor-upload file plus a stakeholder context file:
- **Mentor-upload file:** App Overview, General App Settings, Data Model (canonical types, exact entity syntax), Static Entities, Roles & Permissions (View/Edit/No Access + row-level scoping), Main Features & Screens (recognized UI patterns, dashboard vocabulary), External Integrations (with Data Fabric prerequisites flagged)
- **Context file:** Executive summary, non-functional requirements, acceptance criteria, dependencies & risks, success metrics — for stakeholder sign-off, never uploaded to Mentor

---

## Prerequisites

- OutSystems Docs MCP must be connected (`outsystems-docs` server)
- A problem to solve or requirements to clarify
- 15–30 minutes for interview + research + generation

---

## Tips

1. **Be specific in the interview** — "We need to automate approvals" is more useful than "We need workflow automation"
2. **Mention constraints upfront** — Regulatory requirements, team size, timeline affect app decomposition
3. **Bring existing docs** — If you have notes, an outline, or a problem statement, share it at the start
4. **Review the breakdown** — If the skill proposes multiple apps, confirm the boundaries make sense before finalizing

---

## Next Steps After Generation

1. Review the BRD(s) with stakeholders
2. Get sign-off on scope and requirements
3. Upload to Mentor App Generator
4. Refine Mentor's generated code based on specific business logic
5. Plan deployment and user training

---

## Questions?

Refer to `SKILL.md` for the workflow overview, `system-prompt.md` for detailed instructions and templates, and `Mentor-Requirement-Doc-Standards.md` for the canonical Mentor document vocabulary (data types, UI patterns, dashboard elements, include/avoid rules) — kept current via live MCP research, not just this cached file. `resources/` holds OutSystems' own official sample requirement documents for reference.
