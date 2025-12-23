# AuditMind

**An API-first, audit-safe AI decision explainability and drift analysis platform**

AuditMind is a backend system designed to **store, audit, explain, and analyze decision-making systems** using immutable data models and auditable AI outputs. It combines strong software engineering practices with real LLM-based reasoning to support **regulatory, compliance, and risk analysis use cases**.

This project focuses on **AI governance**, not AI automation.

---

## Why AuditMind?

In real-world systems (finance, healthcare, insurance, enterprise SaaS):

* Decisions must be **immutable**
* Explanations must be **post-hoc**, not decision-making
* AI outputs must be **auditable and traceable**
* Model reasoning must be **inspectable over time**

AuditMind is built to address these requirements from first principles.

---

## Core Design Principles

* **Append-only data model** – no updates, only new versions
* **Separation of concerns** – facts vs interpretations
* **Async AI execution** – AI never blocks core APIs
* **LLM auditability** – model name, prompt hash, timestamps stored
* **Version-aware reasoning** – AI compares decisions across time

---

## System Architecture (High Level)

1. Client submits a decision via API
2. Decision is stored immutably with versioning
3. Async background task triggers AI explanation
4. LLM generates explanation based only on provided inputs/outputs
5. Explanation is stored in a separate, append-only table
6. Optional AI comparison analyzes drift between decision versions

---

## Data Model Overview

### Decisions (Facts)

* Immutable decision records
* Versioned by `decision_key`
* Stores input payload, output payload, metadata

### Decision Explanations (AI Interpretations)

* Linked to a specific decision version
* Stores LLM-generated explanation
* Includes model name, prompt hash, timestamp

### Decision Comparisons (AI Reasoning)

* Compares two versions of the same decision
* Detects changes, consistency, and potential drift
* Fully auditable and append-only

---

## API Capabilities

### Create Decision

* `POST /decisions/`
* Stores a new decision version
* Triggers async AI explanation

### Get Decision History

* `GET /decisions/{decision_key}`
* Returns full immutable audit trail

### Compare Decision Versions

* `POST /decisions/{decision_key}/compare?version_a=&version_b=`
* LLM performs cross-version reasoning
* Flags consistency or drift

---

## AI Capabilities

AuditMind uses a Large Language Model strictly for:

* Post-hoc explanation of decisions
* Confidence and uncertainty articulation
* Cross-version comparison and drift detection

The AI **never**:

* Makes decisions
* Mutates stored facts
* Acts as a source of truth

This ensures regulatory and audit safety.

---

## Tech Stack

* **Backend**: Python, FastAPI
* **Database**: PostgreSQL
* **ORM & Migrations**: SQLAlchemy, Alembic
* **AI**: OpenAI API (LLM-based reasoning)
* **Async Execution**: FastAPI BackgroundTasks
* **Containerization**: Docker, Docker Compose

---

## Running Locally

### Prerequisites

* Docker
* Docker Compose
* OpenAI API key

### Setup

1. Create a `.env` file at project root:

```env
OPENAI_API_KEY=your_api_key_here
```

2. Build and run:

```bash
docker compose up --build
```

3. Access API docs:

```
http://localhost:8000/docs
```

---

## Example Usage

### Create a Decision

```bash
curl --request POST \
  --url http://localhost:8000/decisions/ \
  --header 'Content-Type: application/json' \
  --data '{
    "decision_key": "credit-check-001",
    "input_payload": {"income": 85000, "country": "IN"},
    "output_payload": {"approved": true},
    "decision_made_by": "system"
  }'
```

### Compare Versions

```bash
curl --request POST \
  --url "http://localhost:8000/decisions/credit-check-001/compare?version_a=1&version_b=2"
```

---

## What This Project Demonstrates

* Strong backend engineering fundamentals
* Production-grade database design
* Real-world AI governance patterns
* Async AI pipelines
* Auditable and explainable AI systems

This project is intentionally **not** a UI-heavy demo. It focuses on **system correctness, auditability, and AI safety**.

---

## Future Extensions

* Authentication and role-based access
* Batch drift analysis across decision sets
* Model performance monitoring
* Cost-aware AI scheduling
* UI dashboard for auditors and compliance teams

---

## Author

**Swapnil Bhattacharya**
Software Engineer / Data Science Graduate

---

## License

MIT License
