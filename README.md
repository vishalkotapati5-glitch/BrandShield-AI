# BrandShield AI

Brand-governance platform that reviews content against approved guidelines, facts and assets before publication,
explains every finding, and keeps humans in control. **Status: Stage 0 (foundation).**

## Quick start (local)

```bash
cp .env.example .env
docker compose up -d db                 # Postgres 16 + pgvector

cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head                    # enables pgvector, creates tables
pytest -q                               # Stage 0 test gate
uvicorn app.main:app --reload           # http://localhost:8000/docs

cd ../frontend
cp .env.example .env
npm install && npm run dev              # http://localhost:5173
```

Check `http://localhost:8000/api/v1/health/db`: expect `{"status":"ok","database":"connected","pgvector":true}`.

## Roadmap
| Stage | Scope | Status |
|---|---|---|
| 0 | Repo, Docker DB, Alembic, config, CI, error envelope | written, pending local run |
| 1 | Auth, RBAC, org isolation, audit logs | next |
| 2-8 | Knowledge base, review engine, corrections, workflow, visual auditor, analytics, deploy | planned |

See `docs/` for decisions and disclosures. All sample data will be clearly labelled as sample.
