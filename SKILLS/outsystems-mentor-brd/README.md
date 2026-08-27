# OutSystems Mentor BRD Builder Skill

## Overview

This skill generates Business Requirements Documents (BRDs) for building with OutSystems Mentor App Generator on ODC.

### What makes it different

- **Interactive interview** — asks clarifying questions instead of assuming requirements
- **Multi-app aware** — automatically detects if your requirements need multiple coordinated apps
- **Mentor-grounded** — researches actual Mentor capabilities via OutSystems Docs MCP, not generic templates
- **Ready to upload** — output is formatted to go directly into Mentor App Generator

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
BRD-[AppName]-[YYYY-MM-DD].md
```

One complete BRD covering scope, workflows, integrations, acceptance criteria, and success metrics.

### Multiple Apps

```
00-BRD-Architecture-[ProjectName]-[YYYY-MM-DD].md  ← Start here
01-BRD-[AppName1]-[YYYY-MM-DD].md
02-BRD-[AppName2]-[YYYY-MM-DD].md
...
```

- **Architecture doc** shows app boundaries, dependencies, integration map, and build sequencing
- **Individual BRDs** are self-contained and ready for Mentor upload

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
Creates BRDs with:
- Executive summary grounded in Mentor capabilities
- Detailed workflows and user stories
- Non-functional requirements (performance, security, compliance)
- Integration architecture
- Acceptance criteria & success metrics
- Documented dependencies and risks

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

Refer to `SKILL.md` for the workflow overview and `system-prompt.md` for detailed instructions and templates.
