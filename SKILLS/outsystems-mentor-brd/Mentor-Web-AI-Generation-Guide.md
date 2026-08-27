# Mentor Web AI Generation Guide

**Purpose:** Step-by-step guide for generating multi-app systems with AI Agent apps in Mentor App Generator  
**Target User:** Anyone uploading AI-enabled BRDs to Mentor Web  
**Last Updated:** 2026-08-08

---

## Quick Overview

When you have an AI-enabled BRD set (Backend + Frontend + AI Agent), Mentor Web generation follows this workflow:

```
Backend (30 min)
    ↓
AI Agent (40 min, in parallel with Frontend)
    ↓
Frontend (40 min, after Backend published)
    ↓
Integration Testing (30 min)
```

**Total Time:** ~2 hours to MVP

---

## The Mentor Web Generation Prompts

The skill generates ready-to-paste prompts for each BRD. When you upload a BRD to Mentor Web and it asks **"Build this app?"**, simply paste the appropriate prompt from your BRD file.

### Where to Find Prompts

In each BRD file, look for sections like:

**Section 4B: Mentor Web Generation Prompts**
- "Multi-App Backend Mentor Prompt"
- "Multi-App Frontend Mentor Prompt"
- "Multi-App AI Agent Mentor Prompt"

Copy-paste the relevant prompt for each app generation.

---

## Step-by-Step: Generate Backend

### Prerequisites
- Mentor Web account with ODC access
- `01-BRD-[ProjectName]-Backend.md` (Backend BRD)
- Any shared libraries already published (Integration Connectors Library)

### Steps

**1. Create New App in Mentor Web**
```
Home → "Create New App" → 
App Name: "[ProjectName] Backend"
Description: "Core data, workflows, integrations"
App Type: Standard (not AI Agent)
```

**2. Upload BRD**
```
Click "Upload BRD" → Select `01-BRD-[ProjectName]-Backend.md`
Mentor will parse the BRD and show a summary
```

**3. Mentor Asks "Build this app?"**
```
Paste the Backend Mentor Prompt from your BRD:

"Generate [ProjectName] Backend app with:
- Data entities: Customer, Conversation, ConversationMessage, KnowledgeArticle, 
  Workflow, WorkflowInstance, Agent (7 core + 4 static)
- Business logic: Conversation management, AI orchestration, workflow automation, 
  escalation, analytics, external integrations
- Integrations: CRM (bidirectional), ERP (bidirectional), Email (AWS SES), 
  SMS, WhatsApp, S3, Contact Center, IdP
- Service actions: ~12 public actions (GetConversations, CreateMessage, 
  EscalateConversation, GenerateAIResponse, TriggerWorkflow, GetAnalytics, etc.)
- Integration library: Consume Integration Connectors Library functions
- Performance: Response <500ms (p95), uptime 99.95%
- Important: Do NOT include UI screens, user-facing features, or AI Agent Builder. 
  This Backend will call a separate AI Agent app for intelligence."
```

**4. Review Blueprint**
Mentor generates a blueprint. Verify:
- [ ] All 7 core entities present (check data relationships)
- [ ] All 4 static entities for lookups
- [ ] Service actions listed and correct count (~12)
- [ ] Integration Connectors Library consumption shown
- [ ] No UI screens (correct - Backend only)
- [ ] Entities are data-centric, not UI-centric

If issues, click "Adjust" and provide clarification.

**5. Approve & Generate**
```
Click "Approve" → Mentor generates code (2–5 minutes)
→ Download generated app OR click "Publish to Dev"
```

**6. Publish to Development Environment**
```
If not auto-published:
Apps → [Generated Backend App] → Click "Publish"
Select environment: Development
```

**✅ Backend is now ready for testing and for Frontend to consume**

---

## Step-by-Step: Generate AI Agent (In Parallel)

### Prerequisites
- Mentor Web account with ODC access
- `03-BRD-[ProjectName]-AI-Agent.md` (AI Agent BRD)
- Understanding of AI Agent Builder concepts (tool calling, reasoning flows)

### Important: AI Agent Generation is Different

Mentor Web has a special mode for **AI Agent apps** using OutSystems AI Agent Builder. This is NOT a standard app generation — it's agentic app scaffolding.

### Steps

**1. Create New App in Mentor Web**
```
Home → "Create New App" → 
App Name: "[ProjectName] AI Agent"
Description: "Intelligent decision-making with multi-step reasoning"
App Type: Select "AI Agent" (or "Agentic App") ← KEY DIFFERENCE
```

**2. Upload BRD**
```
Click "Upload BRD" → Select `03-BRD-[ProjectName]-AI-Agent.md`
Mentor will recognize this as an AI Agent BRD
```

**3. Mentor Asks "Build this app?"**
```
Paste the AI Agent Mentor Prompt from your BRD:

"Generate [ProjectName] AI Agent using OutSystems AI Agent Builder with:

SERVICE ACTION (Public Interface):
- GenerateAIResponse(conversationId, customerMessage, conversationHistory)
  Returns: {response, confidenceScore, reasoningTrace, recommendedActions}

TOOLS (Tool Calling):
- SearchKnowledgeBase(query) → retrieves articles from S3/KB
- LookupCustomer(customerId) → retrieves customer data from CRM
- CheckInventory(sku) → queries ERP for availability
- TriggerEscalation(conversationId, reason) → routes to Backend for agent routing

REASONING FLOWS:
- Flow 1 (Simple): Analyze intent → Search KB → If confident, return response
- Flow 2 (Complex): Lookup customer + inventory → Combine context → Generate response
- Flow 3 (Escalation): If confidence < 80%, identify specialization → Route to agent

CONTEXT & MEMORY:
- Retain last 10 messages per conversation
- Store customer sentiment + profile
- Reset after resolution or escalation

LLM:
- Azure OpenAI or Amazon Bedrock
- Model: GPT-4 or equivalent (configurable)
- Temperature: 0.7 (balance creativity + accuracy)

PERFORMANCE & THRESHOLDS:
- Response time: <2 seconds (including tool calls)
- Confidence threshold: 80% for direct response
- <80% confidence triggers Flow 3 (escalation)
- Tool call retry: Exponential backoff, max 2 retries

INTEGRATION:
- Backend app will call this AI Agent service action
- AI Agent can also call Backend service actions (for escalation routing)"
```

**4. Review AI Agent Blueprint**
Mentor shows an AI Agent-specific blueprint. Verify:
- [ ] Service action defined: GenerateAIResponse()
- [ ] Tools listed: SearchKnowledgeBase, LookupCustomer, CheckInventory, TriggerEscalation
- [ ] Reasoning flows visualized (Flow 1, 2, 3)
- [ ] LLM integration configured (Azure OpenAI or Bedrock)
- [ ] Confidence thresholds set (80%)
- [ ] Context management: last 10 messages retained
- [ ] Escalation logic: routes back to Backend

If issues, click "Adjust" and clarify tool definitions or reasoning steps.

**5. Approve & Generate**
```
Click "Approve" → Mentor generates AI Agent code (3–5 minutes)
→ Download generated app OR click "Publish to Dev"
```

**6. Publish to Development Environment**
```
If not auto-published:
Apps → [Generated AI Agent App] → Click "Publish"
Select environment: Development
```

**✅ AI Agent app is now ready. Can run tests with mock Backend**

---

## Step-by-Step: Generate Frontend (After Backend Published)

### Prerequisites
- Backend app already published to development
- Mentor Web account with ODC access
- `02-BRD-[ProjectName]-Frontend.md` (Frontend BRD)

### Important: Frontend Depends on Backend

Frontend generation requires you to reference the published Backend app so Mentor can auto-discover Backend service actions.

### Steps

**1. Create New App in Mentor Web**
```
Home → "Create New App" → 
App Name: "[ProjectName] Frontend"
Description: "User interfaces for 4 roles (Customer, Agent, Supervisor, Admin)"
App Type: Standard
```

**2. Upload BRD**
```
Click "Upload BRD" → Select `02-BRD-[ProjectName]-Frontend.md`
Mentor will parse and display Frontend requirements
```

**3. Mentor Asks "Select Backend Reference"**
```
Dropdown: Select "[ProjectName] Backend" (published in development)
Mentor will query Backend and auto-discover service actions:
- GetConversations()
- CreateMessage()
- EscalateConversation()
- GenerateAIResponse()
- TriggerWorkflow()
- GetAnalytics()
- UpdateConfiguration()
- ManageKnowledgeArticle()
- ManageWorkflow()
- ... (12 total)
```

**4. Mentor Asks "Build this app?"**
```
Paste the Frontend Mentor Prompt from your BRD:

"Generate [ProjectName] Frontend app with:

SCREENS (12 total):
Customer (3): Chat Interface, Conversation History, Self-Service Portal
Agent (3): Agent Dashboard, Conversation Escalation Detail, Active Conversations List
Supervisor (2): Monitoring Dashboard, Performance Analytics
Admin (4): Integration Configuration, Knowledge Base Management, 
          Workflow Configuration, User & Role Management

ROLE-BASED ACCESS CONTROL:
- Customer: See own conversations only
- Agent: See assigned conversations + team metrics
- Supervisor: See all conversations + full analytics
- Admin: See all configuration screens

SERVICE ACTIONS (from Backend):
- Use Backend.GetConversations() for all list screens
- Use Backend.CreateMessage() for chat input
- Use Backend.EscalateConversation() for agent routing
- Use Backend.GenerateAIResponse() for AI chat responses
- Use Backend.GetAnalytics() for dashboards
- All other CRUD operations via Backend service actions

UI LIBRARY:
- Consume UI Components Library for consistent theming
- Use standard patterns: message bubbles, KPI cards, charts, tables, modals

IMPORTANT:
- Frontend is stateless and presentation-only
- All business logic delegated to Backend via service actions
- Role-based visibility: hide/show screens based on authenticated user role
- No local data storage; every action calls Backend"
```

**5. Review Frontend Blueprint**
Mentor shows Frontend blueprint. Verify:
- [ ] 12 screens present (count them)
- [ ] Screens organized by role (Customer/Agent/Supervisor/Admin)
- [ ] Service actions wired: GetConversations, CreateMessage, EscalateConversation, etc.
- [ ] Role-based access shown: screens filtered by role
- [ ] Charts/dashboards for Analytics screens
- [ ] Forms for Configuration screens
- [ ] Message UI for Chat Interface
- [ ] Tables for Active Conversations, Knowledge Base, etc.

If issues, click "Adjust" and clarify screen layouts or action wiring.

**6. Approve & Generate**
```
Click "Approve" → Mentor generates Frontend code (3–5 minutes)
→ Download generated app OR click "Publish to Dev"
```

**7. Publish to Development Environment**
```
If not auto-published:
Apps → [Generated Frontend App] → Click "Publish"
Select environment: Development
```

**✅ Frontend is now published and wired to Backend**

---

## Integration Testing (After All 3 Apps Published)

### Test Flows

**Flow 1: Customer Chat → AI Response**
1. Frontend: Customer role → Chat Interface
2. Customer types: "What's your return policy?"
3. Frontend calls: Backend.GenerateAIResponse(conversationId, message)
4. Backend calls: AI Agent.GenerateAIResponse(conversationId, message)
5. AI Agent:
   - Calls tool: SearchKnowledgeBase("return policy")
   - Gets articles, generates response with confidence score
   - Returns: {response: "...", confidenceScore: 92}
6. Backend stores message, returns to Frontend
7. Frontend displays: AI response + confidence badge + knowledge article links
8. ✅ SUCCESS if: Response appears in <2 seconds

**Flow 2: Low Confidence → Escalation**
1. Customer asks complex question
2. AI Agent generates response, confidence = 45%
3. AI Agent calls: Backend.TriggerEscalation(conversationId)
4. Backend: Finds available agent, assigns conversation
5. Frontend (Agent view): Shows new conversation in queue
6. Agent accepts, sees AI summary + recommended actions
7. Agent sends response to customer
8. ✅ SUCCESS if: Escalation happens within 5 seconds

**Flow 3: Supervisor Monitoring**
1. Supervisor logs in (role = Supervisor)
2. Frontend: Hides Customer/Agent/Admin screens, shows Monitoring Dashboard
3. Frontend calls: Backend.GetAnalytics(dateRange)
4. Backend aggregates: Active conversations, resolved by AI/agent, response times, sentiment
5. Frontend displays: Real-time KPI cards, charts, agent performance table
6. Dashboard auto-refreshes every 5 seconds
7. ✅ SUCCESS if: All metrics display correctly and update in real-time

**Flow 4: Admin Configuration**
1. Admin logs in (role = Admin)
2. Frontend: Shows Integration Configuration screen
3. Admin fills form: CRM API endpoint, key, test connection
4. Frontend calls: Backend.UpdateConfiguration(setting, value)
5. Backend tests connection to CRM, returns success/error
6. ✅ SUCCESS if: Admin receives immediate feedback

### Verification Checklist

After running all flows, verify:

- [ ] **Backend Service Actions**
  - [ ] GetConversations() returns paginated list
  - [ ] CreateMessage() stores messages with timestamp
  - [ ] EscalateConversation() assigns to available agent
  - [ ] GenerateAIResponse() calls AI Agent successfully
  - [ ] GetAnalytics() returns accurate KPIs

- [ ] **AI Agent Integration**
  - [ ] GenerateAIResponse() responds within 2 seconds
  - [ ] Confidence scores are realistic (0–100 range)
  - [ ] Tool calling works (KB search, CRM lookup, ERP check)
  - [ ] Escalation logic triggers on low confidence (<80%)
  - [ ] Reasoning trace provided for debugging

- [ ] **Frontend & Role-Based Access**
  - [ ] Chat Interface loads and accepts input
  - [ ] Agent Dashboard shows active conversations
  - [ ] Supervisor Dashboard shows real-time KPIs
  - [ ] Admin screens show configuration options
  - [ ] Screens hidden for unauthorized roles (Customer can't see Admin screens)

- [ ] **Performance**
  - [ ] Backend responds <500ms to service actions
  - [ ] AI Agent responds <2 seconds (including tool calls)
  - [ ] Frontend screens load <1 second (after Backend responds)
  - [ ] Dashboard auto-refresh every 5 seconds without lag

- [ ] **Data Consistency**
  - [ ] Messages appear in conversation history immediately
  - [ ] Escalations don't duplicate conversations
  - [ ] Analytics aggregate correctly
  - [ ] No orphaned records in database

---

## Common Issues & Troubleshooting

### Issue: AI Agent Generation Fails

**Symptom:** Mentor shows error "Cannot generate AI Agent app"

**Cause:** Mentor couldn't parse tool definitions or reasoning flows

**Fix:**
1. Re-check BRD — verify tool names match exactly (SearchKnowledgeBase, LookupCustomer, etc.)
2. Verify LLM is specified (Azure OpenAI or Bedrock)
3. Re-paste Mentor prompt with clearer tool definitions
4. Contact OutSystems support if error persists

---

### Issue: Frontend Can't Call AI Agent

**Symptom:** Frontend successfully calls Backend, but Backend.GenerateAIResponse() fails

**Cause:** Frontend → Backend integration works, but Backend → AI Agent not wired

**Fix:**
1. Verify AI Agent app is published to same environment
2. In Backend app config, add AI Agent reference (dependency)
3. Republish Backend
4. Test Backend.GenerateAIResponse() directly (use Insomnia or similar)
5. If Backend test succeeds, re-test from Frontend

---

### Issue: Escalation Routes to Wrong Agent

**Symptom:** Customer escalated to unavailable agent

**Cause:** Escalation logic in Backend not checking IsAvailable flag

**Fix:**
1. Review Backend BRD: FR-4.1 should check Agent.IsAvailable = true
2. Check generated Backend code: EscalateConversation() should filter for IsAvailable
3. If not filtering: Adjust Backend code or re-generate with clearer prompt

---

### Issue: AI Response Time Exceeds 2 Seconds

**Symptom:** GenerateAIResponse() takes 5–10 seconds

**Cause:** Tool calls (KB search, CRM lookup) are slow, or LLM latency spike

**Fix:**
1. Check individual tool call times:
   - SearchKnowledgeBase: Should be <500ms (if indexed)
   - LookupCustomer: Should be <1 second (CRM API)
   - CheckInventory: Should be <1 second (ERP API)
2. If tools are slow, optimize queries or add caching
3. Set timeout: If tool call >1 sec, abandon and return lower confidence
4. Consider parallel tool calls (SearchKB + LookupCustomer in parallel)

---

### Issue: Role-Based Access Not Enforced

**Symptom:** Customer can see Agent Dashboard

**Cause:** Frontend role checking logic missing, or Backend not validating user role

**Fix:**
1. Frontend: Verify authenticated user role is passed to Backend with every call
2. Backend: Verify service actions check user role before returning data
3. Example: GetConversations() should filter by CustomerId if role = Customer
4. Re-generate Frontend with stronger role-based screen visibility hints

---

## Success Indicators

You're ready for production when:

✅ **Functional**
- All 12 Frontend screens load and function
- Customer chat → AI response (100% of flows)
- Escalation triggers on low confidence
- Supervisor dashboard updates real-time
- Admin can configure all settings

✅ **Performance**
- Backend: <500ms (p95)
- AI Agent: <2 seconds (p95)
- Frontend: <1 second screen load (p95)
- Dashboard: 5-second refresh without lag

✅ **Reliability**
- No crashes after 1 hour of continuous use
- No data loss during escalation
- Analytics accurate (0 orphaned records)
- Error rate <0.1%

✅ **Security**
- Customer sees only own conversations
- Agent sees only assigned conversations
- Supervisor sees all (read-only)
- Admin can configure (with audit trail)

---

## Next: Staging & Production

After integration testing:

1. **Staging Deployment**
   - Deploy all 3 apps to staging environment
   - Run full UAT with customer team
   - Load testing (simulate 10K concurrent conversations)

2. **Production Deployment**
   - Blue-green deployment recommended
   - Monitoring: Set up alerts for response time, uptime, error rate
   - Runbook: Document escalation procedures for ops team

3. **Post-Launch**
   - Monitor KPIs: AI resolution rate, customer satisfaction, response times
   - Iterate on AI reasoning (improve tool calling, confidence thresholds)
   - Scale if needed (horizontal scaling of Backend + AI Agent)

---

## Questions?

Refer back to:
- **BRD files** for detailed requirements and Mentor prompts
- **Architecture document** for system overview
- **AI Agent Enhancement guide** for AI decision logic

Still stuck? Share the error message and BRD with OutSystems support or your architect.

