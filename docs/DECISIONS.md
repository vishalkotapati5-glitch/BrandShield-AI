# Decisions (defaults proposed in the plan; edit if you chose differently)
1. AI provider: Gemini default, OpenAI swappable behind one interface.
2. Hosting data: Neon/Supabase Postgres (pgvector) + S3-compatible bucket (Cloudflare R2).
3. OCR for scanned PDFs: out of scope for the MVP (documented limitation).
4. Three named improvements: (a) guideline-gap detection, (b) grounding validator with explainability, (c) meaning-preserving corrections with diff and human decision.
