# OutSystems Mentor BRD Skill — AI Agent Enhancement

**Date:** 2026-08-08  
**Purpose:** Reference guide for AI agent architecture decisions in BRD generation  
**Integration:** Referenced by updated system-prompt.md (Phase D interview + Decision Logic)

---

## Overview

This document guides skill users through AI agent architectural decisions. It's referenced during BRD generation when AI capabilities are identified in the interview.

**Key Questions:**
- Q1: What kind of AI? (Simple Q&A vs. Multi-step reasoning)
- Q2: Who owns AI? (Backend team vs. Dedicated AI team)
- Q3: How important is AI? (Nice-to-have vs. Core to product)

**Decision:** Based on answers, recommend Option A (AI in Backend), Option B (Separate AI Agent App), or Option C (AI Library).

---

## Three Options for AI Architecture

### Option A: AI Logic Inside Backend App

**Architecture:**
```
Frontend → Backend App (with embedded AI logic)
```

**When to use:**
- ✅ Simple AI (just Q&A + knowledge lookup + LLM call)
- ✅ MVP/proof-of-concept phase
- ✅ No dedicated AI team
- ✅ Cost-sensitive
- ✅ Tight timeline

**Pros:**
- Fastest to build (2 hours to MVP)
- Simpler architecture (2 apps)
- Lower licensing cost (fewer AOs)

**Cons:**
- AI logic mixed with business logic (harder to maintain)
- AI team can't iterate independently
- Hard to scale AI separately

**BRD Impact:**
- Add to Backend BRD: FR-2 "AI Orchestration & Knowledge Intelligence"
- Describe: LLM calls, knowledge retrieval, confidence scoring, escalation logic
- No new app BRDs needed

---

### Option B: Separate AI Agent App (RECOMMENDED for Production)

**Architecture:**
```
Frontend → Backend → AI Agent App (OutSystems AI Agent Builder)
```

**When to use:**
- ✅ Production system (enterprise platform)
- ✅ Complex AI (multi-step reasoning, tool calling)
- ✅ Dedicated AI team (now or planned)
- ✅ AI is core to product value
- ✅ Need independent AI scaling
- ✅ Future AI evolution planned

**Pros:**
- **Separation of concerns** (business logic vs. AI logic)
- **AI team independence** (iterate without Backend team)
- **Scalable** (AI can scale independently)
- **OutSystems AI Agent Builder features** (multi-step reasoning, tools, memory)
- **Future-proof** (easy to add complex AI features)
- **Reusable** (other apps can call same AI agent)

**Cons:**
- More complex architecture (3 apps)
- More deployment moving parts
- Potentially higher licensing cost

**BRD Impact:**
- Create new: `03-BRD-[ProjectName]-AI-Agent.md`
- Update Backend BRD: "Calls AI Agent app for intelligence" (remove FR-2 detail)
- Update Frontend BRD: Can call AI Agent for responses
- Update Architecture doc: Show 3 apps, AI Agent integration map

---

### Option C: AI Agent Library (Middle Ground)

**Architecture:**
```
Frontend → Backend (uses) → AI Agent Library
```

**When to use:**
- ✅ Medium complexity AI
- ✅ Multiple apps need AI (library reuse)
- ✅ Want to keep 2 apps but organize AI logic
- ✅ Don't need full OutSystems AI Agent Builder features

**Pros:**
- Cleaner than Option A (AI logic separated)
- Simpler than Option B (no 3rd app)
- Reusable across apps

**Cons:**
- AI still tightly coupled to Backend (changes require Backend republish)
- Can't use full AI Agent Builder capabilities
- Less independent than Option B

**BRD Impact:**
- Create library doc: `AI-Agent-Library-BRD.md`
- Update Backend BRD: "Consumes AI Agent Library"
- Frontend BRD unchanged (or references library)
- Architect shows 2 apps + 1 library

---

## Decision Matrix: Which Option to Choose?

### Scoring Guide

**Q1: AI Complexity**
- Simple (just Q&A + KB lookup): +0 points
- Medium (multi-step, some tool calling): +1 point
- Complex (extensive tools, memory, reasoning): +2 points

**Q2: AI Ownership**
- Backend team handles: +0 points
- Future dedicated team: +1 point
- Dedicated AI team now: +2 points

**Q3: AI Importance to Product**
- Nice-to-have feature: +0 points
- Important, will evolve: +1 point
- Core to product value: +2 points

**Q4: System Type (bonus)**
- MVP / Proof-of-concept: +0 points
- Production / Enterprise: +2 points

---

### Recommendations by Score

| Total Points | Recommendation | Rationale |
|---|---|---|
| **0–2** | **Option A (AI in Backend)** | Simple, MVP phase; keep architecture minimal |
| **3–4** | **Option C (AI Library)** | Medium complexity; want reusability without 3rd app |
| **5–6** | **Option B (AI Agent App)** ⭐ RECOMMENDED | Production grade; scalable, future-proof |
| **7+** | **Option B (AI Agent App)** ⭐ STRONGLY RECOMMENDED | Enterprise/critical; needs independence & flexibility |

---

## Implementation Details by Option

### Option A: AI in Backend

**Interview Follow-ups:**
- "What LLM will you use? (Azure OpenAI, Amazon Bedrock, or external service?)"
- "Where is the knowledge base? (S3, file upload, database?)"
- "What confidence threshold for AI response? (default: 80%)"

**BRD Additions to Backend:**

```markdown
### FR-2: AI Orchestration & Knowledge Intelligence

**FR-2.1: Retrieve Knowledge Articles**
- Input: Customer message (natural language query)
- Process: Search knowledge base using semantic matching
- Output: Top 3–5 relevant articles with relevance scores

**FR-2.2: Generate AI Response**
- Input: Customer message + knowledge articles (as context)
- Process: Call external LLM (Azure OpenAI or Bedrock)
- Include: Conversation history (last 5 messages)
- Output: AI response text + confidence score (0–100)

**FR-2.3: AI Resolution Decision**
- If confidence >= 80: Present response to customer
- If confidence < 80: Offer escalation to agent
- Log: All AI attempts for supervisor review

**FR-2.4: Integrate with Workflows**
- Complaint detection (negative sentiment) → Trigger supervisor notification
- Escalation routing → Backend calls available agent
```

**Mentor Prompt:**
```
"This Backend app includes AI orchestration. Add FR-2 logic:
- GenerateAIResponse(message, context) → response, confidence
- SearchKnowledgeBase(query) → articles
- Decision: if confidence >= threshold, return response; else escalate
- Use external LLM (API call); don't embed model"
```

---

### Option B: AI Agent App

**Interview Follow-ups:**
- "What multi-step reasoning flows? (give examples)"
- "What external systems should AI access? (CRM, ERP, KB?)"
- "How complex is the logic? (if/then rules vs. agentic reasoning?)"

**New BRDs Needed:**

1. **Update Backend BRD:**
```markdown
### FR-X: AI Agent Integration

**FR-X.1: Call AI Agent for Intelligence**
- Workflows that need intelligence call Backend service action
- Backend: `TriggerWorkflow(type, conversationId, parameters)`
- If type requires intelligence:
  - Backend calls: `AIAgent.GenerateAIResponse(conversationId, message, context)`
  - AI Agent returns: {response, confidenceScore, reasoning, recommendations}
  - Backend: Stores response + logs reasoning

**Service Action Exposed:**
- `CallAIAgent(conversationId, message, context) → AIAgentResponse`
```

2. **Create AI Agent BRD:**
(See template in system-prompt.md)

---

### Option C: AI Library

**Interview Follow-ups:**
- "Will multiple apps use this AI? (justifies library)"
- "What's the AI interface? (what functions do apps call?)"

**BRDs Needed:**

1. **AI Library BRD:**
```markdown
# AI Agent Library BRD

**Shared AI Logic:** Used by Backend + any other apps needing AI

**Exposed Functions:**
- GenerateResponse(message, context) → response, confidence
- SearchKnowledge(query) → articles
- ClassifyIntent(message) → intent, confidence
- RouteToAgent(intent, constraints) → agentSpecialization
```

2. **Update Backend BRD:**
```markdown
### Libraries Consumed

- **AI Agent Library:** Provides intelligent response generation
  - Call: AILib.GenerateResponse(message, context)
  - Use in: FR-2 AI Orchestration
```

---

## Reference for Interview Questions

**Q8: "Does this system need AI?"**
- Listen for: Yes/No
- If YES → Continue to Q9
- If NO → Proceed with standard architecture

**Q9: "Will you have dedicated AI team?"**
- "No, Backend team handles it"
  - Q10: "Is AI simple (Q&A) or complex (reasoning)?"
    - Simple → Option A
    - Complex → Option B (recommend upgrade)
  
- "Future team, building strategically"
  - → Option B (design for growth)
  
- "Dedicated AI team now"
    → Option B (they own it)

---

## Frequently Asked Questions

### "Can we start with Option A and upgrade to Option B later?"

**Yes, but plan ahead:**
- Write Backend as if Option B exists
- Have Backend call `AIAgent.GenerateResponse()` (mock initially)
- When AI Agent app is ready, just replace the mock with real calls
- Minimize rework

---

### "What's the licensing impact?"

**Option A:** 2 apps = potentially lower AO cost  
**Option B:** 3 apps = potentially higher AO cost (depends on pre-sales answer)

**Guidance:** Get pre-sales confirmation on AO consumption before deciding.

---

### "How does Frontend call AI Agent?"

**Pattern 1 (via Backend):**
```
Frontend calls Backend.CreateMessage()
Backend calls AIAgent.GenerateAIResponse()
Backend returns: {message, aiResponse, confidence}
Frontend displays response
```

**Pattern 2 (direct):**
```
Frontend calls AIAgent.GenerateAIResponse() directly
AI Agent returns response
Frontend displays response
```

**Recommendation:** Pattern 1 (Backend calls AI) keeps data consistency.

---

## Checklist: Use When Detecting AI

**During Interview (Phase D):**
- [ ] Ask Q8: "Does system need AI?"
- [ ] If YES, ask Q9: "Who owns AI logic?"
- [ ] Reference this document for decision matrix

**During Analysis (Part 3):**
- [ ] Score AI complexity + ownership + importance
- [ ] Determine Option A/B/C
- [ ] If Option B, plan for 3-app architecture

**During BRD Generation (Part 4):**
- [ ] If Option A: Expand Backend FR-2
- [ ] If Option B: Create AI Agent BRD + update Backend/Frontend
- [ ] If Option C: Create AI Library + update Backend

**During Output (Part 6):**
- [ ] If Option A: Mention AI in Backend BRD
- [ ] If Option B/C: Explicitly show AI app in architecture diagram

---

## Template Summary

**Option A Template:** See Part 4 of system-prompt.md → Backend BRD → FR-2 expanded

**Option B Template:** See Part 4 of system-prompt.md → "AI Agent App BRD Template"

**Option C Template:** Hybrid of A + B (library exposes AI functions)

---

## Links & References

- **System Prompt:** system-prompt.md (main skill file)
- **Mentor Docs:** Search for "AI Agent Builder" in OutSystems docs
- **DIGI CX Example:** See `/Projects/DIGI-CX/06-AI-AGENT-BRAINSTORM.md`

---

## Version & Updates

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-08 | Initial enhancement; three options (A/B/C) |

**Last Sync:** 2026-07-21 (OutSystems docs MCP)

