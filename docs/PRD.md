# Product Requirements Document (PRD)
## BrandShield AI — AI-Powered Brand Governance and Content Auditing

**Product:** BrandShield AI  
**Repository:** https://github.com/vishalkotapati5-glitch/BrandShield-AI

## 1. Product Overview
BrandShield AI is a web application that helps teams review marketing content against their organisation's brand guidelines. Users can create and manage guidelines, submit content for an AI-assisted audit, inspect findings, and record a human review decision.

AI findings are recommendations. A human reviewer remains responsible for the final decision.

## 2. Problem Statement
Marketing content may be created by different people and across different channels. Without a repeatable review process, content can drift away from approved brand voice, messaging rules, or other documented guidelines. Manually comparing every draft with guidelines can also be time-consuming.

BrandShield AI brings guideline management, AI-assisted checks, findings, and human review into one workflow.

## 3. Product Goals
1. Allow users to create and maintain brand guidelines.
2. Allow users to submit marketing content for an audit.
3. Use Google Gemini to assist with checking submitted content against relevant guidelines.
4. Present findings in a form that a person can understand and review.
5. Allow a human reviewer to approve, reject, or request changes.
6. Preserve audit history and review information in persistent storage.

## 4. Intended Users
- **Brand or marketing team members:** create guidelines and submit content for review.
- **Content creators:** use findings and suggested corrections to improve drafts.
- **Human reviewers:** inspect findings and record a review decision.

These are product personas, not implemented access-control roles. The described version does not include authentication or role-based access control.

## 5. Scope
### In Scope
- Dashboard with audit metrics and recent activity.
- Creation and management of brand guidelines.
- Submission of marketing content for AI-assisted auditing.
- Gemini-powered analysis against saved guidelines.
- Findings with severity, quoted text, explanation, and suggested corrections where available.
- Human review actions: approve, reject, and request changes.
- Audit history and PostgreSQL persistence.

### Out of Scope / Known Limitations
- Authentication and role-based access control.
- Guaranteed correctness of AI results or automatic final decisions.
- Legal, regulatory, or factual verification.
- Integrations with external marketing publishing platforms.

## 6. Functional Requirements

| ID | Requirement | Expected behaviour |
|---|---|---|
| FR-01 | Dashboard | Display audit metrics and recent activity available to the application. |
| FR-02 | Guideline management | Allow users to create and manage brand guideline records. |
| FR-03 | Content submission | Allow users to submit marketing content for an audit. |
| FR-04 | AI analysis | Use relevant content and guideline context for Gemini-assisted analysis. |
| FR-05 | Findings display | Present severity, relevant text, explanation, and suggested correction when returned. |
| FR-06 | Human review | Allow a reviewer to approve, reject, or request changes. |
| FR-07 | Audit history | Persist and display audit records and review state. |

## 7. Non-Functional Requirements
- **Usability:** findings and review actions should be understandable.
- **Maintainability:** UI, API/backend, AI integration, and persistence should have separated responsibilities.
- **Persistence:** guideline and audit information is stored in PostgreSQL.
- **Reliability:** external AI or backend failures should not be silently represented as successful audits.
- **Transparency:** distinguish AI recommendations from human decisions.

## 8. Main User Workflow
1. User opens the dashboard.
2. User creates or selects brand guidelines.
3. User submits marketing content for review.
4. Backend obtains the relevant guideline context and requests Gemini analysis.
5. Application displays returned findings.
6. Human reviewer chooses approve, reject, or request changes.
7. Audit and review information is retained in audit history.

## 9. Acceptance Criteria
- Users can create and manage brand guidelines.
- Users can submit content and receive an AI-assisted result when the AI service is available.
- Findings and suggested corrections are displayed.
- A human reviewer can record a supported review action.
- Audit and review information remains available in persistent history.
- The interface communicates that AI findings are recommendations.

## 10. Success Measures
Success for this project is demonstrated by completing the end-to-end workflow: guideline creation, content submission, AI-assisted analysis, findings display, human decision, and persisted audit history. No production adoption or business-impact metric is claimed.

## 11. Assumptions and Open Points
Exact endpoint paths, request/response schemas, database table names, and deployment configuration must be confirmed from the current source code and environment. Update this document if the implementation changes.
