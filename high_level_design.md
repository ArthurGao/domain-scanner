# High-Level Design

Fist of all, need make decision on the architecture of the application.

There are **two** high-level architecture options for multi-tenant vulnerability-scan platform—one as a single *
*monolith**, the other broken into **microservices**.

Both support:

- **Landing Page & Stripe Pricing**
- **User Onboarding & Multi-Tenant Roles** (with impersonation)
- **Domain/Website Registration & Scan Jobs** (manual or scheduled)
- **Result Storage, Email Notification & Dashboard**
- **Optional AI-powered Reporting**

---

## Option 1: Monolithic Architecture
```
Browser / SPA
     |
     v
Web Server (FastAPI / Spring Boot)
     |
     |--> RDBMS / Graph DB
     |--> Stripe SDK
     |--> Email Service (SMTP)
     |--> Scheduler (Quartz / cron)
     |--> AI Module (Embedded)
```


### Components

1. **Web Server**
    - Single codebase (e.g. FastApi or Django)
    - Serves both the frontend SPA and all REST(Graphql) endpoints
2. **Tenant & User Management**
    - Tables: Users, Organizations, Teams, Roles, Permissions
    - Onboarding flows: email invites, first-user bootstrap
    - Impersonation handled via a special “actAs” JWT claim
3. **Subscription & Billing**
    - Stripe integration lives in the same app
    - Webhooks update subscription state in DB
4. **Domain Management & Scan Workflow**
    - CRUD endpoints for domains/websites
    - Scheduler (Quartz or OS cron) kicks off scan jobs
    - Scan logic runs in-process (or shell-exec’s a Docker container)
5. **Results & Notifications**
    - Stores scan results in relational tables (or a graph edge model)
    - Sends emails directly via SMTP or SES
    - Dashboard endpoints aggregate trends
6. **AI Reporting**
    - Embedded module (Python jar or Node.js micro-library)
    - Runs summarization on stored results

### Benefits / ShortComes

| Benefits                                 | ShortComes                                          |
|------------------------------------------|-----------------------------------------------------|
| Simple deployment & dev cycle            | Codebase grows monolithic & harder to test in parts |
| Single runtime for auth, billing, scans  | Scaling only by scaling entire app                  |
| No inter-service latency or remote calls | Risk of cascading failures (one bug hits all)       |
| Easier local debugging                   | Difficult to adopt polyglot stacks later            |
| Less DevOps overhead (CI/CD, infra)      | Harder to separate concerns (e.g. billing vs scans) |
| Less time to market (faster MVP)         | Harder to adopt new tech (e.g. AI, ML)              |

---

## Option 2: Microservices Architecture

```
              [Browser / SPA]
                      |
                      v
       +-------------------------------+
       |      API Gateway / Kong       |
       |     (REST / GraphQL entry)    |
       +-------------------------------+
                  |
    +-------------+-------------+-------------+-------------+-------------+-------------+-------------+
    |             |             |             |             |             |             |             |
    v             v             v             v             v             v             v             v
[Auth Service] [User & Tenant] [Billing Svc] [Domain Svc] [Scan Svc] [Result DB] [Notify Svc] [AI Report Svc]

    - Auth Service: issues JWTs, impersonation
    - User & Tenant: org/team/role management
    - Billing Service: Stripe integration, webhooks
    - Domain Registry: domain CRUD, ownership
    - Scan Orchestrator: triggers async scan jobs
    - Results Database: stores scan results
    - Notification Service: sends emails on scan complete
    - AI Reporting Service: summarizes scan findings with LLMs
```

### Services

1. **API Gateway** (Kong / AWS API Gateway)
    - Central entrypoint, JWT validation, rate-limit, routing
2. **Auth Service**
    - Issues JWTs, handles impersonation logic
3. **User & Tenant Service**
    - CRUD for users, orgs, teams, roles, permissions
4. **Billing Service**
    - Stripe integration, webhook consumer, subscription status
5. **Domain Registry Service**
    - Tracks domains/websites owned by tenants
6. **Scan Orchestrator**
    - Optional: Accepts scan requests, enqueues jobs to a queue (e.g. SQS, RabbitMQ)
    - Worker processes (in Docker/ECS) pull jobs and run vulnerability scanners
7. **Results Service**
    - Stores scan outcomes in a graph DB (e.g. Neo4j) or relational plus adjacency tables
    - Exposes query endpoints for trends
8. **Notification Service**
    - Listens for job-complete events, sends emails via SES/SMTP
9. **AI Reporting Service**
    - Independent Python/Node service calling OpenAI/ML models
    - Fetches from Results Service to generate summaries

### Interaction Flow

1. **Browser** → calls **API Gateway** for all actions
2. **Signup** → Gateway → BillingSvc → Stripe → BillingSvc writes to DB
3. **Onboarding** → Gateway → AuthSvc/UserSvc create tenant structures
4. **Add Domain** → Gateway → DomainSvc → publishes “DomainAdded” event
5. **Trigger Scan** → DomainSvc → pushes message → ScanSvc picks up
6. **Scan Worker** → runs scanner → writes to ResultsSvc → emits “ScanComplete”
7. **NotifySvc** → on “ScanComplete” sends email to user
8. **Dashboard** → Gateway → ResultsSvc aggregates trends
9. **AI Report** → Gateway → AIReportSvc fetches from ResultsSvc

### Benefits / ShortComes

| Benefits                                        | ShortComes                                      |
|-------------------------------------------------|-------------------------------------------------|
| Independent scaling of heavy components (scans) | Operational complexity (deployment, monitoring) |
| Clear module boundaries, smaller codebases      | Network latency and inter-service communication |
| Polyglot tech choices per service               | More infra (queues, service discovery, gateway) |
| Teams can own individual services               | Higher DevOps overhead (CI/CD per service)      |
| Easier to adopt new tech (e.g. AI, ML)          | Harder to debug (multiple logs, tracing)        |
| Easier to test in isolation                     | More time to market (MVP takes longer)          |
| Easier to scale up                              | More time to market (MVP takes longer)          |

---

**Recommendation:**

- Start with the **Monolith** if we are aiming for speed of delivery and the team is small.
- Evolve to **Microservices** once scans or AI workloads need dedicated scaling or when clear service ownership emerges.

---

## Tasks

### Onboarding Users to a Multi-Tenant Organization Structure

#### Task Breakdown & Estimation

This section outlines the development tasks required to implement onboarding users to an organization/tenant that has
internal teams or sub-tenants.

#### Tech Stack

- **FastAPI** – Web framework
- **PostgreSQL** – Relational DB
- **SQLAlchemy** – ORM
- **Alembic** – Migrations
- **Pydantic v2** – Data validation

#### Task List

| Task                            | Description                                                                                                  |
|---------------------------------|--------------------------------------------------------------------------------------------------------------|
| **1. Schema Design**            | Design DB tables for tenants, organizations, teams, and users. Includes parent-child (sub-tenant) hierarchy. |
| **2. Alembic Migrations**       | Implement Alembic migrations for all tables.                                                                 |
| **3. Pydantic Models**          | Create `BaseModel` classes for request/response validation.                                                  |
| **4. Auth Integration**         | JWT-based auth or integrate external auth (e.g. Cognito/Auth0/Keycloak).                                     |
| **5. API: Create Tenant**       | POST `/tenants/` - Create a new tenant.                                                                      |
| **6. API: Create Organization** | POST `/organizations/` - Assign to tenant, support sub-tenants.                                              |
| **7. API: Create Team**         | POST `/teams/` - Linked to organization, support team roles.                                                 |
| **8. API: Onboard User**        | POST `/users/` - Create user and assign to team/org/tenant.                                                  |
| **9. Role & Permission Setup**  | Define user roles (admin, manager, viewer) with scope restrictions.                                          |
| **10. API: View Hierarchy**     | GET endpoints to fetch org/team/user tree under a tenant.                                                    |
| **11. Unit Tests**              | Pytest-based tests for each module.                                                                          |
| **12. Documentation**           | Use FastAPI auto-docs (Swagger) + README.                                                                    |
| **13. Error Handling**          | Add custom exceptions, validation errors.                                                                    |
| **14. API test                  | Integrating test                                                                                             |
| **15. CI/CD**                   | Add to GitHub Actions or CircleCI for auto-deploys.                                                          |

**Total Estimated Time: 2 - 3 weeks (~1 week with buffer)**

---

### Sub-Tenant / Internal Team Hierarchy Design

This feature allows each organization/tenant to have:

- Sub-tenants (child tenants within the main tenant)
- Internal teams (departments or units within a tenant)
- Scoped user onboarding and role assignment based on their hierarchical position

#### Additional Considerations

| Task                               | Description                                                                 | Estimated Time |
|------------------------------------|-----------------------------------------------------------------------------|----------------|
| **A. Hierarchical Schema Support** | Extend models to support parent-child tenant relationships.                 | 3–4 hrs        |
| **B. Recursive Query Handling**    | Add logic to fetch users, teams, or data recursively under a parent tenant. | 2–3 hrs        |
| **C. Scoped Access Rules**         | Enforce boundaries so users only access data within their scope.            | 3 hrs          |
| **D. Sub-Tenant API Enhancements** | Add endpoints to list/create/manage sub-tenants and their users.            | 2–3 hrs        |

**Total Additional Time: ~10–13 hrs**

### Onboarding Users to a Multi-Tenant Organization Structure

#### Task Breakdown & Estimation

This section outlines the development tasks required to implement onboarding users to an organization/tenant that has
internal teams or sub-tenants.

#### Tech Stack

- **FastAPI** – Web framework
- **PostgreSQL** – Relational DB
- **SQLAlchemy** – ORM
- **Alembic** – Migrations
- **Pydantic v2** – Data validation

#### 📋 Task List

| Task                               | Description                                                                                                  | Estimated Time |
|------------------------------------|--------------------------------------------------------------------------------------------------------------|----------------|
| **1. Schema Design**               | Design DB tables for tenants, organizations, teams, and users. Includes parent-child (sub-tenant) hierarchy. | 4–6 hrs        |
| **2. Alembic Migrations**          | Implement Alembic migrations for all tables.                                                                 | 2–3 hrs        |
| **3. Pydantic Models**             | Create `BaseModel` classes for request/response validation.                                                  | 2–3 hrs        |
| **4. Auth Integration (optional)** | JWT-based auth or integrate external auth (e.g. Cognito/Auth0).                                              | 4–6 hrs        |
| **5. API: Create Tenant**          | POST `/tenants/` - Create a new tenant.                                                                      | 1–2 hrs        |
| **6. API: Create Organization**    | POST `/organizations/` - Assign to tenant, support sub-tenants.                                              | 2–3 hrs        |
| **7. API: Create Team**            | POST `/teams/` - Linked to organization, support team roles.                                                 | 2 hrs          |
| **8. API: Onboard User**           | POST `/users/` - Create user and assign to team/org/tenant.                                                  | 3 hrs          |
| **9. Role & Permission Setup**     | Define user roles (admin, manager, viewer) with scope restrictions.                                          | 4–5 hrs        |
| **10. API: View Hierarchy**        | GET endpoints to fetch org/team/user tree under a tenant.                                                    | 2–3 hrs        |
| **11. Unit Tests**                 | Pytest-based tests for each module.                                                                          | 4–6 hrs        |
| **12. Documentation**              | Use FastAPI auto-docs (Swagger) + README.                                                                    | 1–2 hrs        |
| **13. Error Handling**             | Add custom exceptions, validation errors.                                                                    | 1–2 hrs        |

**Total Estimated Time: 32–44 hours (~1 week with buffer)**

---

### Main Workflow: Domain Scanning & Reporting

This task handles the core scanning functionality after users and domains are onboarded. It includes manual and
scheduled scans, job execution in various environments, result persistence, email notifications, and dashboard
reporting.

#### Task Breakdown – Domain Scanning Workflow

| Task                             | Description                                                  |
|----------------------------------|--------------------------------------------------------------|
| **1. Domain Management APIs**    | Create, list, and delete domains associated with a user/org. |
| **2. Manual Scan Trigger API**   | POST `/scans/trigger` – Triggers a scan job for a domain.    |
| **3. Scheduled Scan Support**    | Add scheduled scan logic (e.g., APScheduler / pg_timetable). |
| **4. Scan Job Handler**          | Job runner that performs scanning (inside Docker or Cloud).  |
| **5. Result Persistence**        | Save scan results to PostgreSQL (vulnerabilities, metadata). |
| **6. Email Notification System** | Send email when results are ready. Use SMTP or AWS SES.      |
| **7. Result Query API**          | GET `/scans/{domain_id}` – Get results by domain.            |
| **8. Dashboard API**             | Return scan history, status, and trend data for UI.          |
| **9. Unit/Integration Tests**    | For all scan-related components.                             |

**Total Estimated Time: 3 - 4 weeks (~1 week with buffer)**

#### Suggested Tools

| Component           | Tool                                                   | Reason                              |
|---------------------|--------------------------------------------------------|-------------------------------------|
| **Task Scheduling** | `pg_timetable`, `APScheduler`, or `Celery + Redis`     | Support recurring tasks and retries |
| **Scan Jobs**       | Python CLI inside Docker container or AWS Batch        | Isolate long-running compute        |
| **Notification**    | SMTP, AWS SES, or SendGrid                             | Reliable delivery with templates    |
| **Data Storage**    | PostgreSQL with JSONB for flexible result schema       | Good performance and indexing       |
| **Trend Dashboard** | FastAPI endpoint + frontend chart lib (e.g., Chart.js) | Visual insights from scan history   |

> **Note:** Also can use AWS Lambda + EventBridge but need consider cold start times and limits on execution time/Cost
> for High Frequency.
---

### AI-Assisted Analysis and Reporting

This task allows users to leverage AI tools to analyze scan results, extract insights, and generate custom reports or
recommendations. It enhances the platform’s value by turning raw data into actionable intelligence.

#### Task Breakdown – AI Integration

| Task                                 | Description                                                                                                |
|--------------------------------------|------------------------------------------------------------------------------------------------------------|
| **1. Define Use Cases**              | Clarify what the AI should do: summarization, threat analysis, recommendations, etc.                       |
| **2. Data Preparation Layer**        | Create a standardized schema for scan result input to the AI model.                                        |
| **3. LLM Integration**               | Integrate OpenAI, HuggingFace Transformers, or self-hosted LLMs to summarize or interpret results.         |
| **4. Prompt Design**                 | Craft and test effective prompts for summarization, report generation, or alert explanation.               |
| **5. User Request API**              | API for users to trigger summarization or report generation based on scan ID.                              |
| **6. Save and View Reports**         | Store AI-generated reports in the database and provide view/download functionality.                        |
| **7. Feedback Mechanism**            | Allow users to rate or give feedback on the usefulness of the generated content.                           |
| **8. Fine-Tuning or RAG (optional)** | Implement Retrieval-Augmented Generation or fine-tuned models for better accuracy on domain-specific data. |

#### Suggested Tools and Services

| Component                        | Suggested Tools                                  |
|----------------------------------|--------------------------------------------------|
| **LLM Service**                  | OpenAI (GPT-4), Claude, HuggingFace Transformers |
| **Embedding & Search (for RAG)** | FAISS, Weaviate, Milvus                          |
| **Prompt Engineering**           | LangChain, PromptLayer                           |
| **Document Output**              | Markdown, HTML, or PDF                           |
| **Data Storage**                 | PostgreSQL JSONB, S3 (for large reports)         |

**Total Estimated Time: 2 - 3 weeks (Maybe more. Too many new tech need to be investigated)**

---

# Deployment Plan

Outlines two deployment strategies for your multi-tenant vulnerability scan platform, based on the architectural
decision: **Monolith** vs **Microservices**.

---

## Option 1: Monolith Deployment – FastAPI-based

### Suitable For

- MVPs
- Small teams
- Faster iterations

### Infrastructure Components

| Component      | Tool/Service                          |
|----------------|---------------------------------------|
| App Runtime    | Docker container for FastAPI          |
| Reverse Proxy  | NGINX or AWS ALB                      |
| Task Scheduler | pg_timetable or APScheduler           |
| Database       | PostgreSQL (e.g., RDS)                |
| Object Storage | S3 for large AI reports               |
| Email Service  | AWS SES, SendGrid, or SMTP            |
| AI Integration | OpenAI SDK or REST API                |
| Hosting        | AWS EC2, Railway, or Fly.io           |
| CI/CD          | GitHub Actions or Railway Deployments |

### Deployment Architecture

```text
Browser
   │
   ▼
[NGINX or ALB]
   │
   ▼
[FastAPI App (Docker)]
   ├── Internal Scheduler
   ├── AI Module
   ├── Stripe SDK
   ├── SMTP/SES Client
   ▼
[PostgreSQL (RDS)] ←→ [S3 for reports]
```

### DevOps Strategy

- Use docker-compose for local development
- GitHub Actions for CI/CD pipeline
- Secrets managed via GitHub Secrets or AWS Secrets Manager
- Logs via CloudWatch or self-hosted Prometheus + Grafana

---

## Option 2: Microservices Deployment – Containerized Services

### Suitable For

- Large-scale platforms
- Independent scaling
- Dedicated teams per service

### Infrastructure Components

| Component             | Tool/Service                                |
|-----------------------|---------------------------------------------|
| API Gateway           | AWS API Gateway, Kong, or Traefik           |
| Service Communication | REST/gRPC, SQS/SNS, or RabbitMQ             |
| Authentication        | Cognito, Keycloak, or custom JWT Service    |
| Service Runtime       | AWS ECS Fargate, Kubernetes (EKS/GKE)       |
| Database              | PostgreSQL + Neo4j (optional)               |
| Object Storage        | S3                                          |
| Email                 | SES or SendGrid                             |
| AI Service Hosting    | ECS, Lambda, or Modal/HuggingFace Inference |
| CI/CD                 | GitHub Actions + AWS CodeDeploy or ArgoCD   |
| Observability         | OpenTelemetry, CloudWatch, Datadog, Jaeger  |

### Deployment Flow

```text
          [Browser / SPA]
                 ↓
           [API Gateway]
   ┌────────┬─────┬────────┬────────────┐
   │        │     │        │            │
[AuthSvc][UserSvc][Billing][DomainSvc] ...
   │        │     │        │
[PostgreSQL]      │        │
           [SQS/RabbitMQ] ←────────────┐
                  ↓                   │
              [Scan Workers]          │
                  ↓                   │
           [ResultService DB]         │
                  ↓                   │
           [AI Report Service] ←──────┘
                  ↓
                [S3]
```

### DevOps Strategy

- Use Terraform to provision ECS, ALB, RDS, S3, IAM, etc.
- Use Secrets Manager or Parameter Store for config
- Use X-Ray or OpenTelemetry for tracing
- Use EventBridge for scan scheduling
