# List of Issues

This document tracks issues discovered during real-world usage of the application. Each issue follows the SFTDD workflow's Issue Resolution Phase for fixing.

---

## Instructions for Use

1. **Add issues** as you discover them during development or production
2. **Only provide title and description** for each issue
3. **Let AI handle** all metadata (status, timestamps, root cause, resolution, triage)

### Example Issue Format:
```markdown
## 1. Login fails with special characters in password
**Description**: When password contains @ symbol, login returns 500 error
```

The AI will automatically add:
- Status (In Progress → Resolved)
- Timestamp (when issue was created)
- Started Resolution (when work began)
- Resolved (when issue was fixed)
- Root Cause (what caused the issue)
- Resolution (how it was fixed)
- Related Use Case (if applicable)
- Test coverage (which tests cover this fix)

---

## Issue Template

Copy and paste this template when adding a new issue:

```markdown
## [Number]. [Issue Title]
**Description**: [Brief description of the issue, including error messages, steps to reproduce, or unexpected behavior]
```

---

## Issue Resolution Workflow

When you add an issue, the AI will:

1. **Triage**: Determine if this is a separate issue, should be merged with existing issue, or requires a new use case
2. **Red Phase**: Create a failing test that reproduces the issue
3. **Green Phase**: Implement minimal fix to make test pass
4. **Refactor Phase**: Clean up code if needed
5. **Update Documentation**: Mark issue as resolved with details

---

## Example Issues (for reference only - delete these when you start)

### 1. API returns 500 error on invalid input
**Description**: When user submits form with empty email field, API returns 500 instead of 400 with validation error
**Status**: Resolved
**Related Use Case**: Use Case #3 (Form validation)
**Timestamp**: 2026-03-05 10:00:00
**Started Resolution**: 2026-03-05 10:05:00
**Resolved**: 2026-03-05 10:30:00

**Root Cause**: 
- Missing null check in email validation function
- Exception thrown instead of returning validation error

**Resolution**:
- Added null check before email validation
- Return 400 status with error message for empty fields
- Test coverage: `test_form_validation_empty_email`

---

### 2. Database connection timeout in production
**Description**: Application crashes after 30 seconds with "Connection timeout" error when connecting to database
**Status**: Resolved
**Related Use Case**: Use Case #1 (Database initialization)
**Timestamp**: 2026-03-05 11:00:00
**Started Resolution**: 2026-03-05 11:10:00
**Resolved**: 2026-03-05 11:45:00

**Root Cause**:
- Default connection timeout was 30 seconds
- Production database requires longer timeout due to network latency

**Resolution**:
- Increased connection timeout to 60 seconds
- Added retry logic with exponential backoff
- Test coverage: `test_database_connection_timeout`, `test_database_connection_retry`

---

## Tips

- **Be specific**: Include error messages, stack traces, or steps to reproduce
- **One issue at a time**: AI resolves issues sequentially, not in parallel
- **Link to use cases**: If issue relates to existing use case, mention it in description
- **Production bugs only**: Use this for bugs found during testing or production, not for new features (use `00-use-case.md` for features)
