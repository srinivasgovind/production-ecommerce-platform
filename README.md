# Store

A production-grade e-commerce platform, built step by step from a 10-product store to a system designed for 1M+ products and users, with an AI shopping assistant on top.

> 🚧 **Status:** Foundations (F0). The README grows with every stage: architecture diagrams, measured results and design decisions are added as they are built.

## Why this project
Most tutorials stop at "it works on my laptop". This project goes further: every stage is **built, deliberately broken (load tests, failures, race conditions), fixed and measured**, the way production systems are run.

## Roadmap
- [ ] **F0** Foundations: Git, HTTP, SQL, Docker, Python internals, testing
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

## Local setup
```bash
cp .env.example .env   # then fill in local values
uv tool install pre-commit
pre-commit install     # runs secret scanning (gitleaks) before every commit
```
More setup steps will be added as the application is built.
