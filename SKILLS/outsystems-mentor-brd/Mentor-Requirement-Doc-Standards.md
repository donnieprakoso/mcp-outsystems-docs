# Mentor Requirement Document Standards

**Purpose:** Canonical vocabulary and structure rules for documents meant to be **uploaded directly to Mentor App Generator**, distilled from OutSystems' own documentation.

**Referenced by:** `system-prompt.md` (Part 3.5, Part 4)

**Status:** This file is a cached snapshot for fast reference. It is **not a substitute for live research**. Every BRD generation run must re-query the `outsystems-docs` MCP (`search_docs` / `get_doc`) for these topics, because Mentor Web ships new capabilities frequently. If MCP content disagrees with this file, **trust the MCP result** and update this file to match.

**Last verified against MCP:** 2026-09-04 (MCP `last_updated()` reported sync `2026-07-21`; live doc site showed `Last updated: Aug 11, 2026` — a ~3-week gap existed between live docs and MCP sync at verification time. Always compare `last_updated()` against what you find and flag drift to the user if the gap looks material.)

**Source docs (ODC, Mentor Web):**
- `use_requirement_documents` (requirements-doc.md)
- `prompts.md` (Prompts for Mentor Web)
- `capabilities.md` (Capabilities and patterns for Mentor Web)
- `how-it-works.md` (AI app generation in Mentor Web)
- `ai-tools.md` (AI tools for working with Mentor Web)

---

## 1. Supported Formats & Limits

- Accepted upload formats: `.txt`, `.docx`, `.pdf`, `.md`
- Maximum file size: **5 MB**
- This skill outputs `.md` — always compliant on size, but confirm nothing pushes the file near 5 MB (e.g., inlined images — which shouldn't be there anyway, see §7).

---

## 2. Document Structure (the part that gets uploaded to Mentor)

A Mentor-ready requirement document has exactly these sections, in this order. Everything else (executive summaries, KPI tables, risk registers) belongs in a **separate, non-uploaded companion file** — see Part 4 of `system-prompt.md`.

| Section | Required? | Content |
|---|---|---|
| App overview | Yes | Purpose, high-level goals, key users — 1-2 paragraphs |
| General app settings | Optional | Theme name, dark mode, primary color, localization/accessibility notes |
| Data model | Yes | Entities with data types, relationships, static entities and records |
| Roles and permissions | Yes | Roles, entity-level access, row-level rules |
| Main features and screens | Yes | Screen list, UI patterns, dashboard specs, UX notes |
| External integrations | Optional | External data sources, direction, Data Fabric connection names |

Write every section as **nested bullet lists, not tables**. Mentor parses structured prose/lists far more reliably than markdown tables — this is explicit official guidance (see §8) and is exactly how OutSystems' own sample docs (in `resources/`) are written.

---

## 3. Data Model: Entity & Attribute Syntax

### Canonical data types (use only these — do not invent others)

`Identifier` · `Text` · `Boolean` · `DateTime` / `Date` · `Currency` · `Integer` · `Email` · `Phone Number` · `User Identifier`

| Data type | Typical use |
|---|---|
| Identifier | Primary keys, foreign keys, bridging entities |
| Text | Names, descriptions, addresses, free-form notes |
| Boolean | True/false flags (`IsActive`, `RequiresApproval`) |
| DateTime / Date | Timestamps, scheduled dates, deadlines |
| Currency | Monetary values |
| Integer | Quantities, counts, ranking positions |
| Email | Business or personal email addresses |
| Phone Number | Mobile, landline, contact center numbers |
| User Identifier | References to OutSystems users/identities |

### Exact entity syntax (copy this pattern)

```
Entity: Order
This entity is stored locally.
Attributes include:
- Id: An Identifier that serves as the Primary Key
- OrderNumber: Text, an auto-generated unique identifier
- OrderDate: DateTime, timestamp of when the order was placed
- CustomerId: An Identifier that is a Foreign Key to the Customer entity
- StatusId: An Identifier that is a Foreign Key to the OrderStatus static entity

Entity Relationships:
- A Customer can have many Orders (One-to-Many)
- An Order can have many OrderItems (One-to-Many)
```

### External entities

If an entity's data comes from outside ODC, name the exact source connection — Mentor references it by name and the connection must already exist:

```
Entity: Customer
This entity's data is sourced from the "Customers" Salesforce connection.
Attributes include:
- Id: An Identifier that is the Primary Key from Salesforce
- Name: Text, the customer's full name or company name
```

**Hard requirement:** Data Fabric connections must exist in ODC *before* generation. Mentor cannot create the connection for you from a BRD — it can only reference one that's already configured. Always flag this to the user as a pre-generation checklist item when a BRD names an external source.

---

## 4. Static Entities (and the Stateflow behavior they trigger)

```
Entity Name: OrderStatus
Purpose: Defines the possible states of an order throughout its lifecycle
Records: Pending, Confirmed, Processing, Shipped, Delivered, Cancelled
```

Mentor auto-detects status/category-shaped static entities and generates a **stateflow** — a state machine with defined transitions, role-gated transition permissions, and required attributes per transition. If the requirements imply an order-dependent lifecycle (e.g., a ticket can't go from "New" straight to "Closed"), say so explicitly in the static entity's Purpose line or in Main Features & Screens — otherwise Mentor may allow free transitions between all statuses.

---

## 5. Roles & Permissions

Per-entity access levels are exactly: **View**, **Edit**, **No Access**. ("Full Access" in a role description is shorthand for Edit access across every entity — not a distinct permission tier. Don't use it as if it were a fourth level; spell out Edit-access-to-all instead if that's the intent.)

Row-level / ownership scoping is expressed as a qualifier after the access level:

```
Role: Hiring Manager
- NewHire: View Access (own team members only)
- OnboardingTask: Edit Access (only for tasks assigned to the "Hiring Manager" department, for their own new hires)

Role: Employee
- Ticket: Edit Access (own records only, based on the CreatedBy attribute)
```

Name the exact attribute or relationship that scopes the row-level rule (e.g., "based on the CreatedBy attribute") — vague scoping ("their own stuff") won't generate correct authorization rules.

---

## 6. Main Features & Screens

### Recognized UI pattern keywords

Mentor matches these keywords (case-insensitive, flexible plurals — "card list" and "cards list" both work) to entities/attributes mentioned nearby:

| Pattern | Use for | Avoid when | Hard constraint |
|---|---|---|---|
| Table | Dense tabular comparison, many columns | Visual summaries, mobile | — |
| Card list | Visual scanning with key attributes + tags | Wide column comparison | — |
| Gallery | Image-centric content | Text-heavy data | — |
| Master detail | Browse + inspect a record | Very small datasets, entities with dependents | Max 5 attributes in the list/table portion; entities with dependents can't use this pattern |
| List with popup | Quick edit/view without navigating away | >5 non-ID attributes, entities with dependents | Max 5 non-ID attributes — Mentor auto-converts to table above this |
| Card list w/ detail on accordion | Compact browsing, expandable detail | >5 detail fields, need multiple sections open at once | Max 5 detail fields; only one accordion item expands at a time |
| Card list w/ detail in sidebar | Frequent detail editing, list stays visible | — | — |
| List with map | Location context | No location data | — |
| Dashboard | High-level KPIs, metrics, visualization | Detailed record editing/browsing | Dashboard lists: max 5 records, no filters/pagination/edit-navigation |

When an entity exceeds a pattern's attribute limit, Mentor silently substitutes a compatible pattern (e.g., popup → table) — so if precision matters, state the pattern **and** name the attributes you expect on it, so a mismatch is visible during blueprint review rather than after generation.

### Dashboard specification syntax

```
Dashboard should consist of:
- Total Active Orders as a counter
- Pending Orders as a counter
- Orders by Status as a Donut Chart
- Revenue by Month as a Vertical Bar Chart
```

- **Chart types:** Bar, Column, Line, Pie, Donut, Area
- **Aggregation functions:** Count, Sum, Average, Minimum, Maximum
- **Column layouts:** 2–6 equal columns, or asymmetric 2:1 / 3:1 ratios
- **Use the explicit-exclusion pattern** when scope matters: state what should *not* appear, e.g. "Do not add anything else besides these charts. Make sure there are no lists displayed on the dashboard." Real Mentor-generated dashboards otherwise tend to over-add elements.

---

## 7. General App Settings

Optional section for:

- **Theme:** name the exact theme as it appears in the ODC tenant — `Use the "Mentor" theme available in the ODC tenant.` Mentor validates the theme exists and is compatible (must have layout block property + Header/Breadcrumbs/Title/Actions/MainContent placeholders) before applying it. Theme cannot be changed post-generation through Mentor — only in ODC Studio.
- **Dark theme:** `Use a dark theme.` — must be requested in the *initial* input to take effect; can't be toggled later. Mentor also auto-selects dark mode if a requested primary color's luminance pairs better with a dark background (evaluated against WCAG contrast).
- **Primary color:** `Use cyan as the primary color.`
- Localization/accessibility requirements, if any.

---

## 8. Include / Avoid (official guidance — apply to the uploaded file)

**Include:**
- Detailed entity definitions with data types and field purposes
- Explicit relationships (One-to-Many, Many-to-Many)
- Functional requirements — what the app does, how users interact
- Specific UI layout types (gallery, card list, master-detail, table, map view)
- Dashboard specifications (specific charts/counters)
- Business logic and workflows
- Access control details (entity-level and row-level)

**Avoid:**
- **PII** — use placeholder/fictional data in every example and sample record, never real names/emails/phones/IDs
- **Implementation code** or technical instructions
- **Screenshots or embedded images** — not processed
- **Complex tables** — use clear lists and text instead (this is why §2–§6 above are written as lists, not tables)
- **Ambiguous language** — no "user-friendly", "intuitive", "robust"; state the specific, measurable behavior instead

---

## 9. What Happens After Upload (set expectations with the user)

Mentor Web's generation workflow has five phases:

1. **Provide input** — prompt or requirement document
2. **Review the blueprint** — Mentor shows entities/attributes/relationships, roles/permissions, proposed screens, and stateflows *before* generating code. This is the cheapest point to catch a misread requirement — fix it here via natural-language refinement prompts, not after generation.
3. **Generate the app** — blueprint becomes a working ODC app (data model, screens, roles, CRUD/navigation/authorization logic), auto-published to the development stage
4. **Refine with prompts** — post-generation refinement processes requests differently than initial generation: use **focused, single-change prompts** ("add a status filter to the Orders table"), not broad re-descriptions of the whole app
5. **Continue in ODC Studio** — for complex business logic, external integrations beyond Data Fabric, or advanced UI customization

Tell the user to expect step 2 and budget time for it — the blueprint review is where a well-structured requirement document pays off, because corrections there are cheap and corrections after generation are not.

---

## 10. Complementary Tools Worth Mentioning

- **OutSystems Mentor Web prompt coach** — a Google Gemini Gem trained on Mentor Web docs, useful for phrasing questions live during blueprint review.
- **Requirement document generator** — an official prompt template (downloadable from the docs site as `resources/mentor-prompt-generator.txt`) that converts raw meeting notes/transcripts into a structured requirement doc. This skill supersedes it for users already in a Claude Code session, but it's worth knowing about if the user wants a lighter-weight tool for a quick one-off outside this skill.
