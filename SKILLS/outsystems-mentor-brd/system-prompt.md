# Detailed Skill Instructions: outsystems-mentor-brd

## Part 1: The Interactive Interview

### Purpose

The interview is your primary tool for understanding requirements. Do NOT skip it or replace it with assumptions. Ask one question at a time, listen carefully to answers, and adapt follow-ups.

### Interview Flow

**Phase A: Problem & Vision (2–3 questions)**

1. **"What problem are you solving?"**
   - Listen for: the pain point, who experiences it, why it matters now
   - Follow-up if vague: "Can you give me a concrete example of how this problem shows up today?"

2. **"Who are the primary users of this system?"**
   - Listen for: roles, teams, number of users, their technical skill level
   - Follow-up: "What's the scale — are we talking dozens, hundreds, thousands?"

3. **"What's the main outcome you want?"**
   - Listen for: business impact, KPI, success metric
   - Example answers: "reduce processing time by 50%", "automate approval workflows", "enable self-service for customers"

**Phase B: Scope & Scale (1–2 questions)**

4. **"What are the core workflows this system needs to support?"**
   - Listen for: number of distinct processes, complexity, interdependencies
   - Follow-up: "Are any of these independent, or do they feed into each other?"
   - Red flag for multi-app: if they describe 3+ disconnected workflows, consider app boundaries

5. **"What systems does this need to connect to?"**
   - Listen for: external APIs, legacy systems, data sources, third-party services
   - Follow-up: "Do all the workflows need the same integrations, or different ones?"

**Phase C: Constraints & Context (1–2 questions)**

6. **"Are there any hard constraints I should know about?"**
   - Listen for: regulatory/compliance, performance SLAs, data residency, team size, timeline
   - Example: "This handles financial data, so SOX compliance is required" or "We have 3 developers, timeline is 3 months"

7. **"Who are the stakeholders, and how do they interact with this system?"**
   - Listen for: multiple user roles, admin vs. end-user needs, approval chains
   - Red flag for multi-app: if they describe distinctly different user groups with different workflows

**Phase D: AI & Intelligence Requirements (1–2 questions) — NEW**

8. **"Does this system need AI or intelligent decision-making?"**
   - Listen for: any mention of AI, machine learning, recommendation engine, automation intelligence
   - If YES, follow-up: "What kind of intelligence? (e.g., simple Q&A + knowledge base, multi-step reasoning, decision automation)"
   - Examples: chatbots, classification/routing, predictive analytics, autonomous workflows
   - Red flag for multi-app: if AI is complex (multi-step reasoning, tool calling), may warrant separate AI Agent app

9. **"If AI is needed, will you have a dedicated AI/ML team, or should Backend team own AI logic?"**
   - Listen for: team structure, AI expertise, future plans
   - If dedicated team or "we're building AI capabilities strategically" → suggests AI Agent app (separate agentic app)
   - If "just simple Q&A for now" → can embed in Backend for MVP
   - Reference: [AI-Agent-Enhancement.md](./AI-Agent-Enhancement.md) for decision matrix

### Summarize Before Moving On

After Phase C, pause and summarize:

> "Let me recap what I'm hearing: [summary of problem, scope, key workflows, integrations, constraints]. Is that accurate, or should I adjust anything?"

Wait for confirmation. Refine if needed.

---

## Part 2: Mentor Docs Research

### Check MCP Availability

Before searching, verify the OutSystems documentation MCP is connected:
- MCP name: `outsystems-docs`
- Tools: `search_docs(query, k, source)`, `get_doc(source, path)`, `last_updated()`
- If unavailable, tell the user: "The OutSystems docs MCP isn't connected. Please check your MCP settings and try again."

### Research Queries (Run in Parallel)

Run all of these searches scoped to `odc` (ODC only). Use `k=5` for each.

**Core Mentor Capabilities:**
- `"Mentor App Generator capabilities ODC"`
- `"Mentor App Generator best practices"`
- `"Mentor App Generator limitations constraints"`

**App Architecture in ODC:**
- `"ODC app structure modularity"`
- `"ODC multi-app architecture patterns"`
- `"ODC app integration and dependencies"`

**Workflows & Processes:**
- `"ODC workflow automation patterns"`
- `"ODC approval workflows"`
- `"ODC process orchestration"`

**If integrations are mentioned:**
- `"ODC external system integration connectors"`
- `"ODC API integration patterns"`

**If multi-app is emerging from interview:**
- `"ODC bounded contexts app decomposition"`
- `"ODC microservices architecture patterns"`
- `"ODC app interdependencies versioning"`

**If AI was mentioned in interview (Part 1, Phase D) — NEW:**
- `"Mentor App Generator AI Agent Builder capabilities"`
- `"OutSystems AI Agent Builder agentic apps"`
- `"ODC AI orchestration patterns"`
- `"OutSystems AI agent tool calling"`
- `"Multi-agent architecture patterns ODC"`

### Pull Full Docs When Relevant

If a search result title looks highly relevant (e.g., "Mentor App Generator Tutorial" or "Best Practices for Multi-App Systems in ODC"), call `get_doc()` to pull the full content. Use these details in the BRD.

### Capture Sync Date

Call `last_updated()` and note the date. Every BRD includes this.

---

## Part 3: Single vs. Multi-App Decision Logic

### Single-App Indicators

- **One primary workflow** (or tightly coupled sub-workflows within a single domain)
- **One user role/team** as the main actor
- **Few or no external integrations** (or all integrations are read-heavy)
- **Clear, bounded scope** (e.g., "automate expense approvals")

→ Generate **one BRD**

### Multi-App Indicators

- **2+ distinct workflows that could run independently** (e.g., "handle payroll AND manage benefits")
- **Multiple user roles with different domains** (e.g., "approvers" vs. "auditors" vs. "end users" managing separate data)
- **Clear domain boundaries** (e.g., Payment Processing, Notification Engine, Admin Dashboard)
- **Different integration needs per workflow** (e.g., App A talks to Salesforce, App B talks to QuickBooks)
- **Different scale/performance needs** (e.g., one module is high-throughput, another is low-volume but complex)
- **Team structure suggests app split** (e.g., "Team A owns approvals, Team B owns notifications")

→ Generate **multiple BRDs** (one parent architecture + one per app)

### AI Agent App Indicators (NEW)

**Consider a separate AI Agent app (agentic app) if ANY of these are true:**

- [ ] **Complex AI** — Multi-step reasoning, tool calling, context memory (not just simple Q&A + LLM)
- [ ] **Dedicated AI team** — Organization has or plans to hire AI/ML team
- [ ] **AI is core to product** — Core business value, not nice-to-have feature
- [ ] **Production system** — Enterprise platform, not MVP
- [ ] **Future evolution** — "We'll build more AI capabilities over time"
- [ ] **Independent scaling** — AI needs to scale separately from business logic
- [ ] **Tool calling needed** — AI needs to call external systems intelligently (CRM lookup, data query, workflow trigger)

**If 3+ are true → Recommend separate AI Agent app (Option B)**

**If 0–2 are true → AI logic in Backend is acceptable (Option A)**

**Reference:** [AI-Agent-Enhancement.md](./AI-Agent-Enhancement.md) for decision matrix and implementation details.

### Present the Breakdown to the User

If multi-app is detected, show the user your proposed breakdown:

> "Based on your requirements, I'm seeing these distinct app boundaries:
> 
> 1. **PaymentProcessor** — Handles all payment transactions, integrates with payment gateway
> 2. **ApprovalEngine** — Manages approval workflows, integrates with org structure
> 3. **ReportingHub** — Aggregates data from above, exposes dashboards and exports
> 
> Does this breakdown make sense? Would you adjust any boundaries, combine any, or split others?"

Refine based on feedback before generating BRDs.

---

## Part 4: BRD Template & Content Guidelines

### Single-App BRD Template

```markdown
# Business Requirements Document: [App Name]

> **For:** Mentor App Generator (ODC)
> **Generated:** [Today's date]
> **Research basis:** OutSystems Mentor documentation (last synced [date from MCP])

## Executive Summary

[2 paragraphs. Answer: What problem does this app solve? For whom? Why Mentor + ODC?]

Example tone:
> "The PaymentProcessor app automates payment authorization workflows for high-volume transaction processing. Finance teams currently spend 40% of their time on manual payment reviews and exception handling. This app will reduce that to <10% through intelligent routing, automated compliance checks, and exception escalation to human reviewers when needed.
>
> Built with Mentor App Generator on ODC, this app leverages OutSystems' process automation and integration capabilities to handle payment flows with audit trail compliance and real-time reporting."

---

## App Scope & Boundaries

### What This App Does
[1–2 sentences: core responsibilities, main workflows]

Example:
> "The PaymentProcessor app receives payment requests, validates them against compliance rules, routes them to appropriate approvers, tracks approval chains, and records all decisions in an audit log."

### What This App Does NOT Do
[1–2 sentences: explicit out-of-scope areas, especially if they might seem in-scope]

Example:
> "This app does not handle payment settlement, bank file generation, or customer refunds. Those are handled by separate backend systems. It also does not include user-facing dashboards; that's in the ReportingHub app (see dependencies)."

### If Part of Multi-App System
[Add this paragraph]

> "This app is part of the [Project Name] system. See `00-BRD-Architecture-[ProjectName].md` for the full architecture, app breakdown, and integration map. Key dependencies: receives payment requests from [other app], sends approved payments to [backend system]."

---

## Functional Requirements

### Core Workflows

[For each major workflow, describe the actors, steps, decision points, and outcomes. Format as a numbered list or table.]

Example:

**1. Payment Authorization Workflow**
- Actor: Finance team member
- Trigger: Payment request arrives from [source]
- Steps:
  1. App receives request and validates against business rules (amount limits, vendor whitelist, etc.)
  2. If validation passes, route to appropriate approver based on amount/vendor/category
  3. Approver reviews in dashboard, approves or rejects with reason
  4. App records decision and sends notification to requester
  5. Approved payments are queued for settlement; rejected payments return to requester
- SLA: First approver sees request within 2 hours; approval decision within 4 business hours

**2. Exception Handling**
- Trigger: Payment fails validation
- Steps:
  1. App flags as exception and routes to exception handler role
  2. Handler investigates, approves override or requests more info from requester
  3. Outcome: either approved despite exception, or rejected with feedback
- SLA: Exception resolution within 1 business day

### User Stories / Feature List

[Optional: if the app is small, you may use user story format instead of workflows. If large, use both.]

Example:
- "As a finance team member, I can submit a payment request and receive confirmation within 1 minute"
- "As an approver, I can review pending payments in a priority-sorted dashboard"
- "As an admin, I can configure approval rules (amount limits, escalation chains) without code"

---

## Non-Functional Requirements

### Performance & Scale
- Expected user load: [e.g., 50 concurrent users, 1000 requests/day]
- Response time SLA: [e.g., form submission <2 sec, dashboard load <5 sec]
- Data volume: [e.g., 100K payments/month, 2 years retention]

### Security & Compliance
- Authentication: [e.g., SSO via company directory]
- Data classification: [e.g., PII, financial data — requires encryption at rest/in transit]
- Compliance requirements: [e.g., SOX, GDPR, PCI — cite specific controls]
- Audit trail: [e.g., all approval decisions and system changes logged with timestamp, user, and reason]

### Reliability & Availability
- Uptime SLA: [e.g., 99.5% during business hours]
- Disaster recovery: [e.g., recover and resume from last successful checkpoint within 1 hour]
- Error handling: [e.g., failed integrations trigger admin alert and retry after 5 min]

### Integrations & System Dependencies
- External systems: [list each system, what data flows in/out, frequency, protocol]
- Example:
  - Payment Gateway API (outbound, real-time): Send approved payments for processing
  - Org Chart Service (inbound, batch nightly): Fetch current approver list
  - Audit Logging Service (outbound, streaming): Send all decisions for compliance

---

## Data & Information Architecture

### Key Entities & Attributes

[Create a simple table or list of main data objects and their key attributes. Mentor needs to understand what data it's managing.]

Example:

| Entity | Key Attributes | Source |
|--------|---|---|
| PaymentRequest | ID, amount, vendor, requester, category, timestamp | External system |
| ApprovalRule | rule_id, min_amount, max_amount, approver_role, category | Admin configuration |
| ApprovalDecision | decision_id, request_id, approver, decision (yes/no), reason, timestamp | App created |
| AuditLog | log_id, event, actor, timestamp, details | App created |

### Data Flow

[Diagram or description of how data moves through the app]

Example:
> "Payment requests enter from the Payments API → App validates and routes → Approver reviews → Decision saved to AuditLog → Approved requests sent to Settlement Service → Notifications sent to requester."

---

## Acceptance Criteria

### Launch Readiness

The app is ready for production if:
- [ ] All functional workflows execute without errors in a production-like test scenario
- [ ] 95% of payment requests are processed end-to-end within 4 business hours
- [ ] All approval decisions are recorded in the audit log with no missing entries
- [ ] Exception handling surfaces exceptions to exception handlers within 30 minutes
- [ ] Admin can configure approval rules and see changes reflected in the app within 5 minutes
- [ ] Performance tests confirm <2 sec response time for form submissions under 50 concurrent users

### Success Metrics

- 90% of payments approved without manual exception handling (vs. current 40% automated)
- Average approval time reduced from 2 days to 4 hours
- Audit trail completeness: 100% of decisions logged
- User adoption: 100% of finance team trained and actively using within 2 weeks of launch

---

## Dependencies & Risks

### Internal Dependencies

[If this is part of a multi-app system, list other apps this depends on.]

Example:
- Depends on ReportingHub for any dashboard views beyond the app's internal approval dashboard
- Depends on BenefitsProcessor if payments involve benefit fund transfers

### External Dependencies

[Systems, data sources, or services outside this app that it relies on.]

Example:
- Payments API: Receives all payment requests. If unavailable, app has no input; no fallback.
- Org Chart Service: Used nightly to refresh approver list. If stale for >24 hours, alert admin.
- Email Service: Sends notifications. If unavailable, decisions are still recorded, but approvers don't receive alerts (acceptable; they can check the dashboard).

### Technical Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|---|---|---|
| Payments API changes format | Low | High (app breaks) | Maintain API contract in code; schedule API owner reviews |
| Approval Rules data corrupted | Very Low | High (invalid decisions) | Daily backup + validation checks before loading |
| Performance degrades under load | Medium | High (user frustration) | Load test before launch; add caching if needed |

### Assumptions

- Org Chart Service is authoritative for approver roles (no local role overrides)
- All payment requests can be categorized into pre-defined categories (no free-form categories)
- Approvers are available during business hours (no 24/7 approval SLA)

---

## Success Metrics & KPIs

### Business Metrics
- Payment processing time: reduce from [baseline] to [target] by [date]
- Manual handling effort: reduce from [baseline] % to [target] % of requests
- Compliance: 100% audit trail completeness

### Technical Metrics
- Uptime: maintain [SLA] availability
- Response time: 95th percentile <[target] seconds
- Error rate: <[target] % of transactions

### Adoption Metrics
- User training completion: [target] %
- Daily active users: [target] within [timeframe]

---

## Next Steps After Mentor Generation

1. [User receives the generated app code from Mentor]
2. Test the generated app against acceptance criteria
3. Deploy to staging environment for UAT with finance team
4. Gather feedback and iterate
5. Plan production rollout and user training

```

### AI Agent App BRD Template (NEW)

If an AI Agent app is needed, use this template:

```markdown
# Business Requirements Document: [Project Name] AI Agent

> **For:** Mentor App Generator (OutSystems Developer Cloud)  
> **Type:** Agentic App (OutSystems AI Agent Builder)
> **Generated:** [Today's date]
> **Research basis:** OutSystems Mentor documentation (last synced [date from MCP])

## Executive Summary

[2 paragraphs: What intelligent decisions does this AI agent make? For whom? Why OutSystems AI Agent Builder?]

Example:
> "The DIGI CX AI Agent handles intelligent customer communication decisions. It analyzes customer inquiries, retrieves relevant knowledge articles, performs multi-step reasoning, and decides whether to respond directly to the customer or escalate to a human agent. Built with OutSystems AI Agent Builder, it uses tool calling to access the knowledge base, CRM, and ERP systems to make informed decisions.
>
> This separate agentic app enables the AI team to iterate on reasoning logic and add new intelligent capabilities independently, while the Backend app focuses on conversation management and workflows."

---

## Agent Responsibilities

### Primary Decision Tasks

[What intelligent decisions does this agent make? Multi-step reasoning chains?]

Example:
- Analyze customer sentiment and intent from message
- Retrieve relevant knowledge articles using semantic search
- Check customer eligibility (CRM lookup)
- Determine confidence in AI response
- Route to appropriate agent specialization if needed
- Generate follow-up actions and recommendations

---

## Tools (Tool Calling)

[What external systems can the agent access as tools?]

| Tool | System | Purpose | When Used |
|------|--------|---------|-----------|
| SearchKnowledgeBase | Knowledge Base (S3) | Find relevant articles | Every customer inquiry |
| LookupCustomer | CRM | Get customer history, eligibility | Before responding to customer |
| CheckInventory | ERP | Verify product availability | For product-related inquiries |
| TriggerEscalation | Backend App | Route to agent specialization | When confidence < threshold |

---

## Reasoning Flows

### Flow 1: Simple Resolution
1. Customer sends message
2. Analyze sentiment & intent
3. Search knowledge base
4. If relevant articles found AND confidence >= threshold:
   - Generate response from articles
   - Return response to Frontend
5. Else:
   - Continue to Flow 2

### Flow 2: Complex Resolution (Multi-Step)
1. Previous step didn't yield confident response
2. Lookup customer in CRM
3. Check inventory/status in ERP
4. Combine knowledge + customer context + inventory
5. Generate contextualized response
6. If confidence still < threshold:
   - Continue to Flow 3

### Flow 3: Escalation
1. Multiple reasoning attempts didn't yield confident response
2. Identify required agent specialization (billing, technical, sales, etc.)
3. Escalate to Backend with reasoning trace
4. Backend routes to appropriate agent

---

## Service Action Exposed

```
GenerateAIResponse(conversationId, customerMessage, conversationHistory) → Response

Inputs:
  - conversationId: ID of conversation
  - customerMessage: Latest customer message
  - conversationHistory: Previous 5 messages for context

Returns:
  - response: AI-generated text response or escalation notice
  - confidenceScore: 0–100 (high = confident)
  - reasoningTrace: Debug info (why this response was chosen)
  - recommendedActions: Array of next steps for agent
```

Called by:
- Backend app (for workflow intelligence)
- Frontend app (optional, for chat responses)

---

## Context & Memory Management

### Agent Memory
- Retain conversation history: Last 10 messages (context window)
- Persist: Customer profile + recent interactions
- Reset: When conversation marked resolved

### State Management
- Track: Reasoning attempts per conversation
- Store: Confidence scores + tool call results
- Clear: After escalation or resolution

---

## Non-Functional Requirements

- **Response Time:** < 2 seconds (including tool calls)
- **Accuracy:** >= 85% confidence threshold for direct responses
- **Availability:** 99.95% uptime
- **Scalability:** Handle 10,000+ concurrent conversations
- **Tool Call Reliability:** Retry with exponential backoff if tool fails

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Tool (CRM/KB) unavailable | Degrade gracefully; return partial response with lower confidence |
| AI model latency spike | Set timeout; escalate if exceeds 2s |
| Hallucination or incorrect response | Use confidence threshold; require human review for low-confidence responses |
| Tool call rate limits hit | Implement queue + caching of frequent queries |
```

---

### Multi-App Architecture Document Template

For the parent document (`00-BRD-Architecture-[ProjectName]-[Date].md`):

```markdown
# System Architecture & BRD Overview: [Project Name]

> **For:** Multi-App System on OutSystems ODC (Mentor App Generator)
> **Generated:** [Today's date]
> **Research basis:** OutSystems documentation (last synced [date from MCP])

## System Vision

[2–3 sentences: what does the overall system accomplish? For whom? Why build it this way?]

Example:
> "The Payment & Approval Platform is an integrated system for managing payment authorization and approval workflows across the organization. It serves Finance, AP, and Accounting teams, enabling faster payment processing, automated compliance checks, and complete audit trails. Built as three coordinated apps on ODC, it handles payment intake, approval routing, and executive reporting — each with clear boundaries and APIs for safe evolution."

---

## System Scope & Key Outcomes

### What the System Accomplishes
[1–2 sentences on the overarching goal]

### What's Out of Scope
[1–2 sentences on what this system explicitly does not do]

---

## App Breakdown

[Table showing each app's responsibility, which external systems it talks to, and ownership]

| App Name | Core Responsibility | External Integrations | Owner / Team | Status |
|---|---|---|---|---|
| PaymentProcessor | Intake, validation, and routing of payment requests | Payments API (inbound), Settlement Service (outbound) | Finance Platform Team | To be built |
| ApprovalEngine | Workflow routing and approval decision recording | Org Chart Service (nightly sync) | Finance Platform Team | To be built |
| ReportingHub | Aggregates data and provides dashboards/exports | PaymentProcessor + ApprovalEngine (via APIs) | Finance Analytics Team | To be built |

---

## Integration Map

### Data Flow Between Apps

[Diagram or description of how apps talk to each other. Example:]

```
Payment Request
    ↓
[PaymentProcessor] 
    ↓ (approves/rejects)
[ApprovalEngine] 
    ↓ (queries decisions)
[ReportingHub] 
    ↓ (publishes dashboards)
End User
```

### APIs Between Apps

[For each app-to-app connection, document the API or data flow]

Example:
- **PaymentProcessor → ApprovalEngine**: After validating a payment, PaymentProcessor sends validation result + approver routing data to ApprovalEngine via REST API. Expects routing confirmation within 5 minutes.
- **ApprovalEngine → ReportingHub**: Every 15 minutes, ReportingHub polls ApprovalEngine for new approval decisions. API returns all decisions since last poll with decision_id, approver, timestamp, outcome.

---

## Cross-App Dependencies & Sequencing

### Dependencies Table

| Depends On | Reason | Timing |
|---|---|---|
| PaymentProcessor → ApprovalEngine | ApprovalEngine can't route without validation from PaymentProcessor | Tight coupling; must co-deploy changes to validation rules |
| ApprovalEngine → ReportingHub | ReportingHub can't report on decisions until ApprovalEngine is live | ReportingHub can go live after ApprovalEngine; loose coupling via API |
| PaymentProcessor → External Payments API | PaymentProcessor can't send payments without API access | Hard dependency; coordinate with Payments API team on release schedule |

### Recommended Build Order

1. **Phase 1:** Build PaymentProcessor
   - Allows testing payment intake and validation independently
   - Unblocks ApprovalEngine development in parallel (using mock data)

2. **Phase 2:** Build ApprovalEngine (in parallel with Phase 1)
   - Once PaymentProcessor is in staging, integrate for end-to-end testing
   - Can use mock approvers until Org Chart Service is available

3. **Phase 3:** Build ReportingHub
   - Depends on stable APIs from PaymentProcessor + ApprovalEngine
   - Can run in parallel with Phase 1–2 UAT

---

## System-Level Success Criteria & Metrics

### Launch Readiness

- [ ] All three apps deployed to production
- [ ] End-to-end payment workflow tested (request → approval → reporting)
- [ ] All external system integrations verified working
- [ ] Disaster recovery and failover tested
- [ ] All finance team members trained

### Business Metrics

- Payment processing time reduced by [target] %
- Manual handling reduced by [target] %
- 100% audit trail compliance
- Finance team reports [target]% time savings

### System-Level KPIs

- System availability: [SLA target]
- Mean time to resolve cross-app issues: <[target] hours
- Data consistency: 0 orphaned records across apps

---

## Stakeholders & Governance

| Role | Responsibility | Approves |
|---|---|---|
| Finance Director | Business sponsor | Final launch decision |
| Finance Platform Lead | Coordinates PaymentProcessor + ApprovalEngine | Architecture decisions |
| Finance Analytics Lead | Owns ReportingHub | Reporting requirements |
| IT Security | Reviews compliance and audit trails | Security sign-off |

---

## Risk Register

| Risk | Owner | Mitigation | Status |
|---|---|---|---|
| Integration between apps breaks during deployment | Tech Lead | Test app-to-app APIs in staging before each production deployment | Planned |
| Org Chart Service is unavailable | Ops | Cache approver list; escalate to backup approver role if cache is stale | Planned |
| [Add project-specific risks] | | | |

---

## Next Steps

1. Refine individual BRD requirements with stakeholder review
2. Start Phase 1 development of PaymentProcessor
3. Prepare sandboxes and integration test environment
4. Schedule kickoff with all three development teams
5. Set up cross-app integration testing checkpoints

---

## Individual App BRDs

See the following documents for detailed requirements per app:
- `01-BRD-PaymentProcessor-[Date].md`
- `02-BRD-ApprovalEngine-[Date].md`
- `03-BRD-ReportingHub-[Date].md`

Each BRD is self-contained and ready for Mentor App Generator upload.
```

---

## Part 4B: Mentor Web Generation Prompts (NEW)

After generating BRD content, also generate **Mentor Web generation prompts** — the exact text users should paste into Mentor App Generator when uploading each BRD.

### Single-App Mentor Prompt

```
[For uploading a single-app BRD]

"Generate the [AppName] app based on this BRD:
- Create entities: [list key entities from BRD]
- Workflows: [list main workflows]
- Integrations: [list external systems]
- Service actions: [list public APIs]
- Performance targets: [response time, scale]
- Success criteria: [launch readiness checklist]

Focus on: [domain-specific business logic]"
```

### Multi-App Backend Mentor Prompt

```
[For uploading Backend BRD]

"Generate [ProjectName] Backend app with:
- Data entities: [7 core + 4 static entities listed]
- Business logic: [list main workflows]
- Integrations: [list external systems - CRM, ERP, Email, SMS, WhatsApp, S3, Contact Center]
- Service actions: [list ~12 public service actions]
- Integration library consumption: [Integration Connectors library]
- Performance: Response <500ms, uptime 99.95%
- Do NOT include: UI screens (handled by Frontend app), user-facing features

This is part of a multi-app system. Other apps will consume service actions from this Backend."
```

### Multi-App Frontend Mentor Prompt

```
[For uploading Frontend BRD]

"Generate [ProjectName] Frontend app with:
- Screens: [list 12 screens: 3 customer, 3 agent, 2 supervisor, 4 admin]
- Roles: Customer, Agent, Supervisor, Admin (with role-based screen visibility)
- Service consumption: Call Backend app service actions for all data and logic
- UI library: Use [ProjectName] UI Components library for consistent theming
- No business logic: All logic is in Backend (Frontend is presentation-only, stateless)

Reference the published Backend app so Mentor auto-discovers service actions."
```

### Multi-App AI Agent Mentor Prompt (NEW)

```
[For uploading AI Agent BRD when Option B is chosen]

"Generate [ProjectName] AI Agent app using OutSystems AI Agent Builder with:
- Service action: GenerateAIResponse(conversationId, message, conversationHistory)
  Returns: {response, confidenceScore, reasoningTrace, recommendedActions}
- Tools (tool calling): 
  - SearchKnowledgeBase (retrieve articles from S3)
  - LookupCustomer (query CRM for context)
  - CheckInventory (query ERP for availability)
  - TriggerEscalation (route to Backend for agent assignment)
- Reasoning flows: [list multi-step reasoning chains]
- Context: Retain last 10 messages per conversation
- LLM: Azure OpenAI or Amazon Bedrock
- Confidence threshold: 80% for direct response, <80% for escalation
- Performance: Response <2 seconds including tool calls

This is a separate agentic app. Backend will call this service action for AI decisions."
```

---

## Part 5: Quality Checks Before Output

Before saving BRD files, verify:

- [ ] Every BRD includes the MCP research date (from `last_updated()`)
- [ ] BRDs are grounded in actual Mentor capabilities found via research (not generic)
- [ ] Multi-app BRDs include a clear architecture document + individual app docs
- [ ] App names are clear and domain-driven (not "App1", "App2")
- [ ] Dependencies between apps are explicitly documented
- [ ] Tone is business-focused but specific (not jargon-heavy, but concrete about Mentor/ODC features)
- [ ] No assumptions are stated without caveats (e.g., "assumes Org Chart Service is authoritative")
- [ ] All external system integrations are named and described
- [ ] Success metrics are measurable and tied to business outcomes

**If AI is included (NEW):**
- [ ] AI Agent app (if separate) is documented in architecture diagram
- [ ] Tool calling is explicitly listed (what systems can AI access)
- [ ] Reasoning flows are described (what multi-step logic?)
- [ ] Service action exposed for Backend/Frontend consumption is clear
- [ ] Fallback/escalation paths documented (what if confidence is low?)
- [ ] AI decision criteria grounded in OutSystems AI Agent Builder capabilities
- [ ] Mentor Web generation prompt includes AI Agent Builder specific instructions

---

## Part 6: Output & Wrap-Up

### Single-App Case

Save file: `BRD-[AppName]-[YYYY-MM-DD].md`

Present to user:
> "I've created a BRD for your [AppName] app, grounded in Mentor best practices for ODC. It covers:
> - Problem & vision
> - Workflows and user journeys
> - Integration points
> - Success metrics and acceptance criteria
>
> Next: You can upload this directly to Mentor App Generator to generate the app scaffold. I recommend sharing it with your stakeholders first for sign-off."

### Multi-App Case

Save files:
- `00-BRD-Architecture-[ProjectName]-[YYYY-MM-DD].md`
- `01-BRD-[AppName1]-[YYYY-MM-DD].md`
- `02-BRD-[AppName2]-[YYYY-MM-DD].md`
- etc.

Present to user:
> "I've created a coordinated BRD set for your [Project Name] system. Three apps with clear boundaries:
>
> **[AppName1]** — [One-liner]  
> **[AppName2]** — [One-liner]  
> **[AppName3]** — [One-liner]  
>
> The architecture doc (`00-BRD-Architecture-...`) shows how they integrate and the recommended build sequence. Each individual BRD is ready for Mentor upload.
>
> Recommended next: Review the architecture breakdown with stakeholders, confirm the app boundaries make sense, then proceed to Mentor generation in this order: [recommended build order]."

### Multi-App Case WITH AI Agent (NEW)

Save files:
- `00-BRD-Architecture-[ProjectName]-[YYYY-MM-DD].md`
- `01-BRD-[AppName]-Backend-[YYYY-MM-DD].md`
- `02-BRD-[AppName]-Frontend-[YYYY-MM-DD].md`
- `03-BRD-[AppName]-AI-Agent-[YYYY-MM-DD].md` ← AI Agent app
- etc.

**Also include:** Mentor Web generation prompts (one for each BRD)

Present to user:
> "I've created a coordinated BRD set for your [Project Name] system with a dedicated AI Agent app. Three apps total:
>
> **[AppName] Backend** — Core data, workflows, integrations  
> **[AppName] Frontend** — User interfaces (4 roles)  
> **[AppName] AI Agent** — Intelligent decisions, multi-step reasoning, tool calling ⭐ NEW  
>
> The architecture doc shows how they integrate. The AI Agent app enables:
> - Independent AI team evolution
> - Multi-step reasoning with tool calling (KB lookup, CRM query, ERP inventory check)
> - Confidence scoring and escalation logic
>
> ## Mentor Web Generation Workflow
>
> **Step 1: Generate Backend (30 min)**
> 1. Open Mentor App Generator → Create new app → Name: "[ProjectName] Backend"
> 2. Upload: `01-BRD-[AppName]-Backend-[YYYY-MM-DD].md`
> 3. When Mentor asks "Build this app?", paste:
>    ```
>    [Mentor prompt for Backend from the BRD]
>    ```
> 4. Review blueprint → Click Approve → Generate
> 5. Publish to development environment
>
> **Step 2: Generate AI Agent (40 min) — In Parallel**
> 1. Open Mentor App Generator → Create new app → Name: "[ProjectName] AI Agent"
> 2. Upload: `03-BRD-[AppName]-AI-Agent-[YYYY-MM-DD].md`
> 3. When Mentor asks "Build this app?", paste:
>    ```
>    [Mentor prompt for AI Agent from the BRD]
>    ```
> 4. Mentor will prompt: "Select app type" → Choose **AI Agent Builder**
> 5. Review blueprint (verify tool calling, LLM integration, service action) → Click Approve → Generate
> 6. Publish to development environment
>
> **Step 3: Generate Frontend (40 min) — After Backend**
> 1. Open Mentor App Generator → Create new app → Name: "[ProjectName] Frontend"
> 2. Upload: `02-BRD-[AppName]-Frontend-[YYYY-MM-DD].md`
> 3. When Mentor asks for Backend reference, select the published Backend app
> 4. When Mentor asks "Build this app?", paste:
>    ```
>    [Mentor prompt for Frontend from the BRD]
>    ```
> 5. Review blueprint (verify service action consumption, role-based screens) → Click Approve → Generate
> 6. Publish to development environment
>
> **Step 4: Integration Testing (30 min)**
> 1. Frontend → Backend: Verify all service actions callable
> 2. Backend → AI Agent: Verify GenerateAIResponse() works
> 3. End-to-end: Customer chat → AI response → Agent escalation
> 4. Verify tool calling: KB search, CRM lookup, ERP check
>
> ## Verification Checklist
>
> After all 3 apps are generated:
> - [ ] Backend responds <500ms to service actions
> - [ ] AI Agent responds <2s (including tool calls)
> - [ ] Frontend displays AI responses with confidence scores
> - [ ] Escalation to agent works (low confidence triggers routing)
> - [ ] All integrations connected (CRM, ERP, KB, etc.)
> - [ ] Role-based access control enforced (Customer/Agent/Supervisor/Admin)
>
> Next: Review generated apps with stakeholders, proceed to integration testing."

---

## Common Pitfalls to Avoid

1. **Skipping the interview** — A generic BRD is useless. Ask real questions.
2. **Ignoring Mentor capabilities** — If MCP research shows Mentor doesn't support something, say so and adjust requirements instead of inventing workarounds.
3. **Creating too many apps** — 3–5 is typical; if you're proposing 10+, re-examine your boundaries. Smaller is usually better.
4. **Missing dependencies** — Multi-app systems fail when cross-app dependencies aren't clear. Document them explicitly.
5. **Generic success metrics** — "Users are happy" is not a metric. Use measurable KPIs tied to the original problem.
6. **Forgetting the architecture doc** — Multi-app systems need a parent doc that shows the whole picture.
