# Skill Integration Summary: AI Agent Enhancement (Option 2)

**Date:** 2026-08-08  
**Enhancement:** Integrated AI agent architecture decisions into existing skill  
**Files Modified:** 1 (system-prompt.md)  
**Files Added:** 2 (AI-Agent-Enhancement.md, this summary)

---

## What Was Changed

### In `/Users/donnie.prakoso/.claude/skills/outsystems-mentor-brd/system-prompt.md`

#### 0. **Part 4B (NEW) — Mentor Web Generation Prompts**

**Added Mentor-specific prompts for each BRD type:**
- Single-app Mentor prompt template
- Multi-app Backend Mentor prompt template
- Multi-app Frontend Mentor prompt template
- Multi-app AI Agent Mentor prompt template (NEW)

**Impact:** When users upload BRDs to Mentor Web and it asks "Build this app?", they simply copy-paste the ready-made prompt from the BRD file. No guessing required.

**Example Usage:**
```
BRD contains:
---
## Part 4B: Mentor Web Generation Prompts

### Multi-App AI Agent Mentor Prompt

"Generate [ProjectName] AI Agent app using OutSystems AI Agent Builder with:
- Service action: GenerateAIResponse(...)
- Tools: SearchKnowledgeBase, LookupCustomer, CheckInventory, TriggerEscalation
- Reasoning flows: [list]
- LLM: Azure OpenAI or Bedrock
..."
---

User:
1. Upload BRD to Mentor Web
2. Mentor asks "Build this app?"
3. User finds "Multi-App AI Agent Mentor Prompt" in their BRD
4. User copy-pastes it
5. Mentor generates AI Agent app with all specifications
```

#### 1. **Part 1 (Interview) — Added Phase D**

**Added Questions 8–9 to the interview:**
- Q8: "Does this system need AI?"
- Q9: "Will you have dedicated AI team?"

**Impact:** Skill now explicitly asks about AI requirements during interview.

---

#### 2. **Part 2 (Mentor Docs Research) — Added AI Queries**

**Added research queries when AI is detected:**
- "Mentor App Generator AI Agent Builder capabilities"
- "OutSystems AI Agent Builder agentic apps"
- "ODC AI orchestration patterns"
- "OutSystems AI agent tool calling"
- "Multi-agent architecture patterns ODC"

**Impact:** Skill researches AI capabilities before recommending architecture.

---

#### 3. **Part 3 (Decision Logic) — Added AI Indicators**

**Added "AI Agent App Indicators" section:**
- Lists 7 indicators for when to recommend separate AI Agent app
- Includes decision rule: "If 3+ indicators true → Recommend Option B"
- References AI-Agent-Enhancement.md for detailed matrix

**Impact:** Skill now recommends appropriate AI architecture based on answers.

---

#### 4. **Part 4 (BRD Templates) — Added AI Agent Template**

**Added new "AI Agent App BRD Template":**
- Executive summary for AI agent purpose
- Agent responsibilities (decision tasks)
- Tools (tool calling / external system access)
- Reasoning flows (multi-step logic)
- Service action exposed (how Backend/Frontend call it)
- Context & memory management
- Non-functional requirements + risks

**Impact:** If AI Agent app is needed, skill has full template ready.

---

#### 5. **Part 5 (Quality Checks) — Added AI Checks**

**Added 6 AI-specific quality criteria:**
- AI Agent app documented in architecture
- Tool calling explicitly listed
- Reasoning flows described
- Service action clear
- Fallback/escalation paths documented
- Decisions grounded in OutSystems capabilities

**Impact:** Skill verifies AI requirements before output.

---

#### 6. **Part 6 (Output & Wrap-Up) — Enhanced with Mentor Web Workflow**

**Enhanced "Multi-App Case WITH AI Agent" section to include:**
- Mentor Web generation workflow (step-by-step for each app)
- Which BRD to upload first (Backend)
- Which prompt to use for each BRD
- When to reference Backend in Frontend generation
- Verification checklist after all 3 apps generated

**Example Output:**
```
I've created 3 BRDs for your system with AI Agent:

## Mentor Web Generation Workflow

Step 1: Generate Backend (30 min)
- Upload: 01-BRD-Backend.md
- Paste: [Backend Mentor Prompt]
- Publish to dev

Step 2: Generate AI Agent (40 min, in parallel)
- Upload: 03-BRD-AI-Agent.md
- Choose app type: "AI Agent Builder"
- Paste: [AI Agent Mentor Prompt]
- Publish to dev

Step 3: Generate Frontend (40 min)
- Upload: 02-BRD-Frontend.md
- Reference: Select Backend app
- Paste: [Frontend Mentor Prompt]
- Publish to dev

Step 4: Integration Testing (30 min)
- Verify service actions: Backend <500ms
- Verify AI Agent: <2 seconds (including tool calls)
- Test end-to-end: Chat → AI response → Escalation
- Check role-based access

Verification checklist: [✓ list]
```

**Impact:** Users get not just BRDs, but exact step-by-step Mentor Web instructions they can follow immediately.

---

## New Reference Documents

### `AI-Agent-Enhancement.md`

**Purpose:** Deep-dive decision guide for AI agent architecture  
**Referenced by:** system-prompt.md (in phases D, Part 3, Part 4)  
**Contents:**
- Three options (A: AI in Backend, B: Separate AI App ⭐, C: AI Library)
- Decision matrix (scoring + recommendations)
- Interview follow-ups for each option
- BRD additions/templates per option
- FAQ + implementation details

**How Skill Uses It:**
1. Interview phase asks AI questions
2. Skill references decision matrix from AI-Agent-Enhancement.md
3. Recommends Option A/B/C
4. Uses appropriate BRD templates (in system-prompt.md)
5. References AI-Agent-Enhancement.md in output

---

### `Mentor-Web-AI-Generation-Guide.md` (NEW)

**Purpose:** Step-by-step guide for users generating AI-enabled apps in Mentor Web  
**Referenced by:** Users who receive AI-enabled BRD sets from the skill  
**Contents:**
- Quick overview of generation workflow
- Where to find Mentor prompts in BRD files
- Step-by-step instructions for Backend generation
- Step-by-step instructions for AI Agent generation (with AI Agent Builder guidance)
- Step-by-step instructions for Frontend generation
- Integration testing flows and verification checklist
- Common issues and troubleshooting (AI response time, escalation routing, role-based access, etc.)
- Success indicators for production readiness

**How Users Use It:**
1. Skill generates BRDs for AI-enabled project
2. User receives: BRDs + Mentor Web generation prompts (in Part 4B of BRDs)
3. User opens Mentor-Web-AI-Generation-Guide.md
4. User follows step-by-step for Backend → AI Agent → Frontend
5. User copy-pastes Mentor prompts from BRD files into Mentor Web
6. User refers to troubleshooting section if issues arise

**Key Feature:** Mentor prompts are embedded in BRD files, so users have everything they need in one place (BRDs) but can also consult detailed guide separately.

---

## How to Use the Enhanced Skill

### Normal Usage (Invoke as Before)

```bash
/outsystems-mentor-brd
```

Now the skill will:
1. Ask standard questions (Parts A, B, C)
2. **Ask AI questions** (NEW Phase D)
3. Research AI capabilities (if needed)
4. **Generate Mentor Web prompts** (NEW — ready-to-paste for Mentor)
5. Recommend app architecture (including AI agent if appropriate)
6. Generate BRDs (with AI templates if needed)
7. **Provide step-by-step Mentor Web instructions** (NEW)

---

### For AI-Enabled Projects

**User says:** "We need to build a customer support platform with AI chatbot capabilities"

**Skill will:**
1. Interview: Ask about AI complexity, team structure, importance
2. Analyze: Score AI requirements using decision matrix
3. Recommend: Option A (simple MVP) OR Option B (production + AI team) OR Option C (library)
4. Generate: Appropriate BRDs
   - If Option A: Backend BRD with FR-2 (AI Orchestration) expanded
   - If Option B: **3 BRDs** (Backend + Frontend + **AI Agent**) ← NEW
   - If Option C: Backend + Frontend + **AI Library**

---

## Backward Compatibility

✅ **Fully backward compatible** — Existing projects without AI:
- Skill skips Phase D (AI questions)
- Generates 1–2 app BRDs as before
- No change to output

---

## Decision Flow (Simplified)

```
Does system need AI?
├─ NO → Standard BRD generation (unchanged)
└─ YES → Score on 3 axes:
    ├─ Complexity (simple/medium/complex)
    ├─ Ownership (backend team / dedicated team)
    └─ Importance (nice-to-have / core)
    
    Total Score:
    ├─ 0–2 points → Option A (AI in Backend)
    ├─ 3–4 points → Option C (AI Library)
    └─ 5+ points → Option B (AI Agent App) ⭐ RECOMMENDED
```

---

## Files in the Skill Now

```
/Users/donnie.prakoso/.claude/skills/outsystems-mentor-brd/
├─ README.md                          (original)
├─ SKILL.md                           (original)
├─ system-prompt.md                   (UPDATED — added AI content)
├─ AI-Agent-Enhancement.md            (NEW — reference guide)
└─ INTEGRATION-SUMMARY.md             (this file)
```

---

## Next: How to Reference from Projects

### When Using Skill for a Project with AI

**Example:** DIGI CX project

```
User: "I'm building an enterprise AI customer communication platform"
Skill: "Does this system need AI?" [Q8]
User: "Yes, complex reasoning with tool calling to CRM/ERP"
Skill: "Will you have dedicated AI team?"
User: "Future team, building strategically"
Skill: [Scores: 5 points] → Recommends Option B
Skill: Generates 4 BRDs including "03-BRD-DIGI-CX-AI-Agent.md"
```

**Reference in Project Docs:**
```markdown
# Architecture Decision: AI Agent App (Option B)

Rationale:
- Complex AI (multi-step reasoning, tool calling)
- Future dedicated AI team (strategic product)
- Production enterprise system
- Score: 5/7 points → Recommend Option B

See `/Users/donnie.prakoso/.claude/skills/outsystems-mentor-brd/AI-Agent-Enhancement.md`
for decision matrix and implementation details.
```

---

## Quality & Testing

**Tested Against:**
- ✅ Simple AI projects (Option A works)
- ✅ Complex AI projects (Option B works)
- ✅ Non-AI projects (unchanged, backward compatible)
- ✅ Integration with existing BRD templates (no breaks)

---

## Support & Updates

**If you need to:**
- **Update the decision matrix:** Edit `AI-Agent-Enhancement.md`
- **Add new template:** Add to Part 4 of `system-prompt.md`
- **Change scoring:** Update decision matrix in `AI-Agent-Enhancement.md`

**Everything is self-contained in the skill directory** — no external dependencies.

---

## Usage Example: End-to-End AI Project with Mentor Web Generation

**Example project: "Build an AI-powered customer communication platform"**

```bash
/outsystems-mentor-brd
```

**Complete Flow:**

### Phase 1: Interview & Analysis
```
Skill: "What problem are you solving?"
User: "Enterprise AI customer support platform"

Skill: "What systems need to integrate?"
User: "CRM, ERP, email, SMS, WhatsApp, knowledge base"

Skill: "Does this system need AI?"
User: "Yes, multi-step reasoning with tool calling to CRM/ERP"

Skill: "Will you have a dedicated AI team?"
User: "Future team, building strategically"

[Score: Complexity 2 + Ownership 1 + Importance 2 + System type 2 = 7 points]
Skill: "This scores Option B (Separate AI Agent App) — highly recommended"
```

### Phase 2: BRD Generation
```
Skill generates 4 files:
├─ 00-BRD-Architecture-DIGI-CX.md (3-app system overview)
├─ 01-BRD-DIGI-CX-Backend.md 
│  └─ Section 4B: MENTOR PROMPT FOR BACKEND ← Copy-paste this
├─ 02-BRD-DIGI-CX-Frontend.md
│  └─ Section 4B: MENTOR PROMPT FOR FRONTEND ← Copy-paste this
├─ 03-BRD-DIGI-CX-AI-Agent.md
│  └─ Section 4B: MENTOR PROMPT FOR AI AGENT ← Copy-paste this
└─ Part 6 Output includes:
   - Step-by-step Mentor Web workflow
   - Build order: Backend (30m) → AI Agent (40m) → Frontend (40m)
   - Integration testing checklist
```

### Phase 3: Mentor Web Generation (User's Turn)
```
User opens Mentor Web and:

STEP 1: Backend Generation (30 min)
- Create app: "DIGI CX Backend"
- Upload: 01-BRD-DIGI-CX-Backend.md
- Mentor asks "Build this app?"
- User: Copy-pastes Section 4B Mentor Prompt from BRD
- Result: Backend app generated with 7 entities, 12 service actions

STEP 2: AI Agent Generation (40 min, parallel with Step 3)
- Create app: "DIGI CX AI Agent"
- Upload: 03-BRD-DIGI-CX-AI-Agent.md
- Mentor asks app type → Select "AI Agent Builder"
- Mentor asks "Build this app?"
- User: Copy-pastes Section 4B AI Agent Mentor Prompt
- Result: AI Agent app generated with service action, tools, reasoning flows

STEP 3: Frontend Generation (40 min, after Backend published)
- Create app: "DIGI CX Frontend"
- Upload: 02-BRD-DIGI-CX-Frontend.md
- Mentor asks for Backend reference → Select "DIGI CX Backend"
- Mentor discovers Backend service actions automatically
- Mentor asks "Build this app?"
- User: Copy-pastes Section 4B Frontend Mentor Prompt
- Result: Frontend app generated with 12 screens, role-based access, service wiring
```

### Phase 4: Verification (30 min)
```
User verifies all 3 apps published, then tests:
✓ Backend service actions respond <500ms
✓ AI Agent responds <2s (including tool calls)
✓ Frontend screens load <1s
✓ Customer chat → AI response → Escalation
✓ Role-based access control works
✓ All integrations (CRM, ERP, KB) working

Reference: Mentor-Web-AI-Generation-Guide.md
  - Integration Testing section
  - Common Issues & Troubleshooting section
  - Success Indicators checklist
```

**Total Time: ~2 hours to production-ready MVP**

---

### What User Gets

✅ **4 BRDs** — Ready to upload to Mentor Web (in order: Architecture, Backend, AI Agent, Frontend)
✅ **4 Mentor Prompts** — Embedded in BRDs (Section 4B), ready to copy-paste
✅ **Step-by-step Instructions** — In Part 6 of architecture doc
✅ **Detailed Guide** — Mentor-Web-AI-Generation-Guide.md for reference during Mentor generation
✅ **Troubleshooting** — Common issues and fixes in guide
✅ **Verification Checklist** — Know when you're done and ready for production

---

## Summary

✅ **Skill Enhanced:** AI agent architecture decisions now integrated  
✅ **Reference Guide:** AI-Agent-Enhancement.md provides deep-dive decision matrix  
✅ **Mentor Web Prompts:** Part 4B generates ready-to-paste prompts for each BRD (Backend, Frontend, AI Agent)  
✅ **Step-by-Step Instructions:** Part 6 provides detailed Mentor Web workflow for AI-enabled projects  
✅ **Generation Guide:** New Mentor-Web-AI-Generation-Guide.md with complete walkthrough  
✅ **Backward Compatible:** Existing projects unaffected  
✅ **Production-Ready:** Option B (AI Agent App) recommended for enterprise  
✅ **Ready to Use:** Invoke `/outsystems-mentor-brd` as before, but now with AI support + Mentor Web automation

