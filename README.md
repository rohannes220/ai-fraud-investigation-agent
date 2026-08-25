# AI Fraud Investigation Agent

An explainable, portfolio-scale financial-crime investigation application.

**Transactions → fraud rules → alerts → AI evidence review → investigator case note**

## What it does
- Generates reproducible synthetic bank transactions
- Stores customers, transactions, alerts, and investigations in PostgreSQL
- Flags unusual transaction size, rapid large transfers, repeated near-threshold transfers, and multiple new counterparties
- Assigns transparent risk scores
- Uses an LLM to draft an evidence-grounded case note
- Provides a FastAPI backend and browser investigation dashboard
- Does not use an ML fraud classifier

## Run
```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d db
PYTHONPATH=. python scripts/init_db.py
PYTHONPATH=. python scripts/seed_data.py
PYTHONPATH=. python scripts/run_rules.py
PYTHONPATH=. uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000`.

Add `OPENAI_API_KEY` to `.env` for LLM-written reports. Without it, the app uses a simple deterministic fallback report.

## Why rules instead of ML?
The project is about AI-assisted investigation rather than predictive modeling. Rules make detection transparent and auditable; the LLM handles the language-heavy investigation summary.

## Interview explanation
I built a fraud investigation application that separates detection from investigation. Explainable Python rules scan transaction histories for suspicious patterns. Alerts are stored in PostgreSQL and passed to an LLM with the underlying transaction evidence. The model drafts a case note but is explicitly instructed not to declare that fraud occurred.

## Resume bullet
Built an AI-assisted fraud investigation platform using Python, SQL, FastAPI, PostgreSQL, and LLMs to identify explainable suspicious transaction patterns and generate evidence-grounded investigator case reports.

All customers and transactions are synthetic. This is an educational portfolio project, not a production fraud-detection system.
