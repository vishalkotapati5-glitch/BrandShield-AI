
import { useEffect, useState } from "react";
import {
  ShieldCheck, LayoutDashboard, ScanSearch, BookOpen,
  ClipboardCheck, History, Plus, RefreshCw, CheckCircle2,
  AlertTriangle, XCircle, Clock, Menu, X, Send,
  FileText, Activity, ChevronRight, Loader2
} from "lucide-react";
import { api } from "./api/client";

type Page = "Dashboard" | "AI Auditor" | "Guidelines" | "Review Center" | "Audit History";

type Finding = {
  guideline: string;
  severity: string;
  problem: string;
  suggestion: string;
  quoted_text: string;
};

type Audit = {
  id: string;
  submitted_content: string;
  overall_status: string;
  summary: string;
  findings: Finding[];
  review_status: string;
  created_at?: string;
};

type Guideline = {
  id: string;
  title: string;
  category: string;
  rule: string;
};

type Health = {
  status: string;
  version: string;
};

const navigation = [
  { name: "Dashboard" as Page, icon: LayoutDashboard },
  { name: "AI Auditor" as Page, icon: ScanSearch },
  { name: "Guidelines" as Page, icon: BookOpen },
  { name: "Review Center" as Page, icon: ClipboardCheck },
  { name: "Audit History" as Page, icon: History },
];

function statusColor(status: string) {
  const value = status?.toLowerCase() ?? "";
  if (["pass", "approved", "approve", "compliant", "safe"].includes(value))
    return "status-green";
  if (["fail", "rejected", "reject", "critical", "high"].includes(value))
    return "status-red";
  if (["warning", "needs_review", "request_changes", "medium"].includes(value))
    return "status-yellow";
  return "status-purple";
}

function App() {
  const [page, setPage] = useState<Page>("Dashboard");
  const [health, setHealth] = useState<Health | null>(null);
  const [audits, setAudits] = useState<Audit[]>([]);
  const [guidelines, setGuidelines] = useState<Guideline[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mobileMenu, setMobileMenu] = useState(false);

  const [content, setContent] = useState("");
  const [auditResult, setAuditResult] = useState<Audit | null>(null);

  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("Marketing");
  const [rule, setRule] = useState("");

  const [reviewComment, setReviewComment] = useState("");
  const [selectedAudit, setSelectedAudit] = useState<Audit | null>(null);

  async function loadData() {
    setLoading(true);
    setError("");

    try {
      const [healthData, auditData, guidelineData] = await Promise.all([
        api<Health>("/health"),
        api<Audit[]>("/reviews"),
        api<Guideline[]>("/guidelines"),
      ]);

      setHealth(healthData);
      setAudits(Array.isArray(auditData) ? auditData : []);
      setGuidelines(Array.isArray(guidelineData) ? guidelineData : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load dashboard data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function runAudit(e: React.FormEvent) {
    e.preventDefault();
    if (!content.trim()) return;

    setLoading(true);
    setError("");
    setAuditResult(null);

    try {
      const result = await api<Omit<Audit, "id" | "review_status">>(
        "/audits",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content }),
        }
      );

      const newAudit = result as Audit;
      setAuditResult(newAudit);
      await loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "The audit could not be completed.");
    } finally {
      setLoading(false);
    }
  }

  async function addGuideline(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !rule.trim()) return;

    setLoading(true);
    setError("");

    try {
      await api("/guidelines", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, category, rule }),
      });

      setTitle("");
      setRule("");
      await loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save guideline.");
    } finally {
      setLoading(false);
    }
  }

  async function makeDecision(
    audit: Audit,
    decision: "approve" | "reject" | "request_changes"
  ) {
    setLoading(true);
    setError("");

    try {
      await api(`/reviews/${audit.id}/decision`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          decision,
          reviewer_comment: reviewComment,
        }),
      });

      setReviewComment("");
      setSelectedAudit(null);
      await loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save your decision.");
    } finally {
      setLoading(false);
    }
  }

  const pendingAudits = audits.filter(
    (audit) => !audit.review_status || audit.review_status === "pending"
  );

  const approvedAudits = audits.filter(
    (audit) => audit.review_status === "approve"
  );

  const flaggedAudits = audits.filter(
    (audit) => ["fail", "warning", "needs_review"].includes(
      audit.overall_status?.toLowerCase()
    )
  );

  function renderFinding(finding: Finding, index: number) {
    return (
      <div className="finding-card" key={index}>
        <div className="finding-top">
          <span className="finding-number">Finding {index + 1}</span>
          <span className={`status-pill ${statusColor(finding.severity)}`}>
            {finding.severity}
          </span>
        </div>
        <h4>{finding.guideline}</h4>
        {finding.quoted_text && (
          <blockquote>"{finding.quoted_text}"</blockquote>
        )}
        <p><strong>Issue:</strong> {finding.problem}</p>
        <p><strong>Suggestion:</strong> {finding.suggestion}</p>
      </div>
    );
  }

  function renderDashboard() {
    return (
      <>
        <div className="welcome-row">
          <div>
            <p className="eyebrow">OVERVIEW</p>
            <h1>Dashboard</h1>
            <p className="muted">Your brand compliance workspace at a glance.</p>
          </div>
          <button className="secondary-button" onClick={loadData}>
            <RefreshCw size={16} /> Refresh
          </button>
        </div>

        <div className="stats-grid">
          <StatCard icon={FileText} label="Total Audits" value={audits.length} />
          <StatCard icon={Clock} label="Pending Reviews" value={pendingAudits.length} />
          <StatCard icon={CheckCircle2} label="Approved" value={approvedAudits.length} />
          <StatCard icon={AlertTriangle} label="Flagged Audits" value={flaggedAudits.length} />
        </div>

        <div className="dashboard-grid">
          <section className="panel">
            <div className="panel-heading">
              <div>
                <h2>Recent Audits</h2>
                <p className="muted">Latest content compliance checks</p>
              </div>
              <button className="text-button" onClick={() => setPage("Audit History")}>
                View all <ChevronRight size={15} />
              </button>
            </div>

            {audits.length === 0 ? (
              <EmptyState message="No audits yet. Submit your first piece of content to get started." />
            ) : (
              <div className="audit-list">
                {audits.slice(0, 5).map((audit) => (
                  <div className="audit-row" key={audit.id}>
                    <div className="audit-icon"><FileText size={18} /></div>
                    <div className="audit-info">
                      <strong>{audit.submitted_content?.slice(0, 65) || "Content audit"}</strong>
                      <span>{audit.summary}</span>
                    </div>
                    <span className={`status-pill ${statusColor(audit.overall_status)}`}>
                      {audit.overall_status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="panel quick-panel">
            <h2>Quick Actions</h2>
            <p className="muted">Jump straight into your workflow.</p>
            <button className="quick-action" onClick={() => setPage("AI Auditor")}>
              <span className="quick-icon purple"><ScanSearch size={19} /></span>
              <span><strong>Audit Content</strong><small>Check content with AI</small></span>
              <ChevronRight size={17} />
            </button>
            <button className="quick-action" onClick={() => setPage("Guidelines")}>
              <span className="quick-icon blue"><BookOpen size={19} /></span>
              <span><strong>Manage Guidelines</strong><small>Set your brand rules</small></span>
              <ChevronRight size={17} />
            </button>
            <button className="quick-action" onClick={() => setPage("Review Center")}>
              <span className="quick-icon green"><ClipboardCheck size={19} /></span>
              <span><strong>Review Content</strong><small>Make human decisions</small></span>
              <ChevronRight size={17} />
            </button>
          </section>
        </div>
      </>
    );
  }

  function renderAuditor() {
    return (
      <>
        <PageHeading title="AI Content Auditor" subtitle="Check your content against your brand guidelines." />
        <div className="two-column">
          <section className="panel">
            <h2>Submit Content</h2>
            <p className="muted">Paste the text you want BrandShield AI to inspect.</p>
            <form onSubmit={runAudit} className="form-stack">
              <label htmlFor="audit-content">Content to audit</label>
              <textarea
                id="audit-content"
                rows={12}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste your marketing copy, social media post, advertisement, or other brand content here..."
                required
              />
              <div className="form-footer">
                <span className="muted">{content.length} characters</span>
                <button className="primary-button" disabled={loading || !content.trim()}>
                  {loading ? <Loader2 className="spin" size={17} /> : <ScanSearch size={17} />}
                  {loading ? "Checking..." : "Run AI Audit"}
                </button>
              </div>
            </form>
          </section>

          <section className="panel info-panel">
            <div className="large-icon"><ShieldCheck size={30} /></div>
            <h2>What does the auditor check?</h2>
            <p className="muted">The AI reviews submitted content using your saved brand guidelines.</p>
            <div className="check-item"><CheckCircle2 size={17} /> Brand terminology</div>
            <div className="check-item"><CheckCircle2 size={17} /> Marketing claims</div>
            <div className="check-item"><CheckCircle2 size={17} /> Brand consistency</div>
            <div className="check-item"><CheckCircle2 size={17} /> Potential compliance issues</div>
            <div className="note-box">
              <strong>Human review matters.</strong>
              <p>AI findings are recommendations. A human reviewer makes the final decision.</p>
            </div>
          </section>
        </div>

        {auditResult && (
          <section className="panel result-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">AUDIT COMPLETE</p>
                <h2>Audit Results</h2>
              </div>
              <span className={`status-pill ${statusColor(auditResult.overall_status)}`}>
                {auditResult.overall_status}
              </span>
            </div>
            <p className="result-summary">{auditResult.summary}</p>
            <h3>Findings ({auditResult.findings?.length ?? 0})</h3>
            {auditResult.findings?.length ? (
              auditResult.findings.map(renderFinding)
            ) : (
              <EmptyState message="No findings were returned for this audit." />
            )}
            <p className="muted">This audit has been saved for human review.</p>
          </section>
        )}
      </>
    );
  }

  function renderGuidelines() {
    return (
      <>
        <PageHeading title="Brand Guidelines" subtitle="Define the rules your AI auditor should follow." />
        <div className="two-column">
          <section className="panel">
            <h2>Add a Guideline</h2>
            <form onSubmit={addGuideline} className="form-stack">
              <label htmlFor="guideline-title">Guideline title</label>
              <input id="guideline-title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Brand terminology" required />
              <label htmlFor="guideline-category">Category</label>
              <select id="guideline-category" value={category} onChange={(e) => setCategory(e.target.value)}>
                <option>Marketing</option>
                <option>Tone of Voice</option>
                <option>Terminology</option>
                <option>Legal & Compliance</option>
                <option>Visual Identity</option>
                <option>Other</option>
              </select>
              <label htmlFor="guideline-rule">Rule description</label>
              <textarea id="guideline-rule" rows={5} value={rule} onChange={(e) => setRule(e.target.value)} placeholder="Describe what content should or should not do..." required />
              <button className="primary-button" disabled={loading}>
                <Plus size={17} /> Save Guideline
              </button>
            </form>
          </section>

          <section className="panel">
            <div className="panel-heading">
              <div>
                <h2>Saved Guidelines</h2>
                <p className="muted">{guidelines.length} rules configured</p>
              </div>
              <BookOpen size={21} />
            </div>
            {guidelines.length === 0 ? (
              <EmptyState message="No guidelines saved yet. Add your first brand rule." />
            ) : (
              guidelines.map((item) => (
                <div className="guideline-card" key={item.id}>
                  <span className="category-tag">{item.category}</span>
                  <h3>{item.title}</h3>
                  <p>{item.rule}</p>
                </div>
              ))
            )}
          </section>
        </div>
      </>
    );
  }

  function renderReviews() {
    return (
      <>
        <PageHeading title="Human Review Center" subtitle="Review AI findings and make the final content decision." />
        {pendingAudits.length === 0 ? (
          <section className="panel">
            <EmptyState message="You're all caught up. There are no pending reviews." />
          </section>
        ) : (
          <div className="review-layout">
            <section className="panel">
              <h2>Pending Reviews ({pendingAudits.length})</h2>
              {pendingAudits.map((audit) => (
                <button
                  className={`review-item ${selectedAudit?.id === audit.id ? "selected" : ""}`}
                  key={audit.id}
                  onClick={() => {
                    setSelectedAudit(audit);
                    setReviewComment("");
                  }}
                >
                  <div>
                    <strong>{audit.submitted_content?.slice(0, 65) || "Content audit"}</strong>
                    <small>{audit.findings?.length ?? 0} findings · {audit.overall_status}</small>
                  </div>
                  <ChevronRight size={17} />
                </button>
              ))}
            </section>

            <section className="panel">
              {selectedAudit ? (
                <>
                  <div className="panel-heading">
                    <h2>Review Details</h2>
                    <span className={`status-pill ${statusColor(selectedAudit.overall_status)}`}>
                      {selectedAudit.overall_status}
                    </span>
                  </div>
                  <h3>Submitted Content</h3>
                  <div className="submitted-text">{selectedAudit.submitted_content}</div>
                  <h3>AI Summary</h3>
                  <p className="muted">{selectedAudit.summary}</p>
                  <h3>Findings</h3>
                  {selectedAudit.findings?.length ? selectedAudit.findings.map(renderFinding) : <p className="muted">No findings.</p>}
                  <label htmlFor="review-comment">Reviewer comment</label>
                  <textarea id="review-comment" rows={3} value={reviewComment} onChange={(e) => setReviewComment(e.target.value)} placeholder="Add your review notes (optional)..." />
                  <div className="decision-buttons">
                    <button className="approve-button" disabled={loading} onClick={() => makeDecision(selectedAudit, "approve")}><CheckCircle2 size={16} /> Approve</button>
                    <button className="reject-button" disabled={loading} onClick={() => makeDecision(selectedAudit, "reject")}><XCircle size={16} /> Reject</button>
                    <button className="secondary-button" disabled={loading} onClick={() => makeDecision(selectedAudit, "request_changes")}><RefreshCw size={16} /> Request changes</button>
                  </div>
                </>
              ) : (
                <EmptyState message="Select a pending audit to review its content and findings." />
              )}
            </section>
          </div>
        )}
      </>
    );
  }

  function renderHistory() {
    return (
      <>
        <PageHeading title="Audit History" subtitle="A record of content checks and their review status." />
        <section className="panel">
          {audits.length === 0 ? (
            <EmptyState message="Your audit history will appear here." />
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr><th>Submitted Content</th><th>AI Result</th><th>Human Decision</th><th>Summary</th></tr>
                </thead>
                <tbody>
                  {audits.map((audit) => (
                    <tr key={audit.id}>
                      <td className="content-cell">{audit.submitted_content?.slice(0, 75)}</td>
                      <td><span className={`status-pill ${statusColor(audit.overall_status)}`}>{audit.overall_status}</span></td>
                      <td><span className={`status-pill ${statusColor(audit.review_status)}`}>{audit.review_status || "pending"}</span></td>
                      <td className="summary-cell">{audit.summary}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </>
    );
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileMenu ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-mark"><ShieldCheck size={24} /></div>
          <div><strong>BrandShield</strong><small>AI COMPLIANCE</small></div>
          <button className="mobile-close" onClick={() => setMobileMenu(false)}><X size={20} /></button>
        </div>

        <p className="nav-label">WORKSPACE</p>
        <nav>
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.name}
                className={`nav-item ${page === item.name ? "active" : ""}`}
                onClick={() => { setPage(item.name); setMobileMenu(false); }}
              >
                <Icon size={19} />
                <span>{item.name}</span>
                {item.name === "Review Center" && pendingAudits.length > 0 && (
                  <span className="nav-count">{pendingAudits.length}</span>
                )}
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="connection-card">
            <span className={`connection-dot ${health ? "online" : "offline"}`} />
            <div><strong>{health ? "API Connected" : "API Disconnected"}</strong><small>{health ? `Version ${health.version}` : "Check backend server"}</small></div>
          </div>
          <div className="user-card">
            <div className="avatar">BS</div>
            <div><strong>BrandShield Team</strong><small>Workspace Admin</small></div>
          </div>
        </div>
      </aside>

      {mobileMenu && <button className="mobile-overlay" aria-label="Close menu" onClick={() => setMobileMenu(false)} />}

      <main className="main-area">
        <header className="topbar">
          <button className="mobile-menu" onClick={() => setMobileMenu(true)}><Menu size={22} /></button>
          <div className="breadcrumb">Workspace <span>/</span> <strong>{page}</strong></div>
          <div className="topbar-right">
            <span className={`connection-label ${health ? "connected" : ""}`}>
              <span className="connection-dot" /> {health ? "System online" : "Connecting"}
            </span>
            <button className="icon-button" title="Refresh data" onClick={loadData}><RefreshCw size={18} /></button>
          </div>
        </header>

        <div className="page-content">
          {error && (
            <div className="error-banner">
              <AlertTriangle size={18} />
              <span>{error}</span>
              <button onClick={() => setError("")}><X size={16} /></button>
            </div>
          )}

          {page === "Dashboard" && renderDashboard()}
          {page === "AI Auditor" && renderAuditor()}
          {page === "Guidelines" && renderGuidelines()}
          {page === "Review Center" && renderReviews()}
          {page === "Audit History" && renderHistory()}

          <footer className="footer">
            <span>BrandShield AI</span>
            <span>AI-assisted compliance · Human final decision</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

function PageHeading({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="welcome-row">
      <div><p className="eyebrow">BRANDSHIELD WORKSPACE</p><h1>{title}</h1><p className="muted">{subtitle}</p></div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value }: { icon: typeof FileText; label: string; value: number }) {
  return (
    <div className="stat-card">
      <div className="stat-icon"><Icon size={21} /></div>
      <p>{label}</p>
      <strong>{value}</strong>
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="empty-state">
      <div className="empty-icon"><Activity size={24} /></div>
      <p>{message}</p>
    </div>
  );
}

export default App;
