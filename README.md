# Store

A production-grade e-commerce platform, built step by step from a 10-product store to a system designed for 1M+ products and users, with an AI shopping assistant on top.

> 🚧 **Status:** S0, the store monolith (project skeleton done). The README grows with every stage: architecture diagrams, measured results and design decisions are added as they are built.

## Why this project
Most tutorials stop at "it works on my laptop". This project goes further: every stage is **built, deliberately broken (load tests, failures, race conditions), fixed and measured**, the way production systems are run.

## Roadmap
- [x] **F0** Foundations: Git, HTTP, SQL, Docker, Python internals, testing
- [ ] **S0** Store monolith: FastAPI + PostgreSQL, tests, CI
- [ ] **S1** First real deploy on AWS with CI/CD
- [ ] **S2** Payments, concurrency and a flash sale (10K users, zero overselling)
- [ ] **S3** Cloud scale (100K users): caching, search, Terraform
- [ ] **S4** Microservices and event-driven design with Kafka (1M users)
- [ ] **S5** Platform scale: Kubernetes (EKS), multi-region, Black Friday readiness
- [ ] **S6** Amazon-level system design
- [ ] **S7** AI layer: RAG product search and a customer-support agent

## Tech stack (planned)
Python 3.12 · FastAPI · PostgreSQL · Redis · Docker · GitHub Actions · AWS · Terraform · Kafka · Kubernetes · Prometheus · Grafana · OpenTelemetry

## Project layout
```
src/store/
├── main.py          # app factory: builds the FastAPI app, plugs in routers
├── api/             # HTTP in/out: requests → service calls, results → status codes
├── services/        # business rules (no HTTP, no SQL)
├── domain/          # what things ARE: Product, Order
└── repositories/    # the only layer that knows how data is stored
tests/unit/          # fast tests, no database
tests/integration/   # tests against real Postgres (from S0 step 3)
```

## Local setup
Requires [uv](https://docs.astral.sh/uv/). uv installs the pinned Python (3.12) and exact dependencies from `uv.lock`.
```bash
uv sync                          # create .venv with exact dependencies
uv run pre-commit install        # gitleaks, ruff, mypy before every commit
uv run pytest                    # run the tests
uv run uvicorn store.main:app --reload   # start the API → http://127.0.0.1:8000/docs
```

## Quality gates
Every commit (pre-commit) and every PR (GitHub Actions CI) runs: **gitleaks** (secrets), **ruff** (lint + format, including blocking calls in async code), **mypy --strict** (types) and **pytest**.
