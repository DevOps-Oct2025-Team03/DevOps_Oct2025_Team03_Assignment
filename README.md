# DevOps_Oct2025_Team03_Assignment
## Project Overview

This project is a DevSecOps **Minimum Viable Product (MVP) built using Flask to serve as a reusable template for secure software delivery.** The application implements authentication and role-based authorization, providing two main user experiences: an Admin Dashboard for managing user accounts and a User Dashboard for managing uploaded files. Admin users can create and delete user accounts, while regular users can upload, download, and delete their own files. 

A core security requirement is strict data isolation: each user must only be able to view and access files that they own. This is enforced in both the backend logic and the database design where files must be tied to a valid owner.

From a DevSecOps perspective, the repository is designed to demonstrate a secure delivery pipeline where code changes are validated automatically through CI on GitHub Actions, including automated testing and container builds. **The goal is to show how security and quality checks can be integrated into the commit-to-deploy process without slowing down development, providing a standardized blueprint that future teams can adopt.**

## Stakeholders (Context)
This project is designed to support the following stakeholders:

- **Centre Appointment Holders**  
  Provides a standardized and consistent deployment and CI approach across teams.

- **Future Development Teams / Industrial Partners**  
  Serves as a reusable project and CI/CD template to bootstrap future applications.

- **Security Compliance Office**  
  Establishes the foundation for automated quality and security checks through CI.


## Repository Structure
```text
DevOps_Oct2025_TeamXX_Assignment/
│
├── app/                         # Flask application package
│   ├── __init__.py              # App factory (creates Flask app)
│   ├── routes.py                # Basic routes (/ and /health)
│   ├── config.py                # Configuration (env-based)
│   ├── database.py             
│   │
│   ├── templates/               # HTML templates 
│   │   └── .gitkeep
│   │
│   └── static/                  # CSS / JS / images
│       └── .gitkeep
│
├── tests/                       # Automated tests
│   ├── __init__.py
│   ├── test_basic.py            # Sanity test for CI
|   ├── test_data_isolation.py   # Ownership constraint tests
|   ├── conftest.py              # Test configuration & DB fixtures
|   └── test_security.py         # Bcrypt hashing verification
│
├── .github/                     # GitHub configuration
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
│
├── docs/                        # Documentation & evidence
│   └── evidence/
│       ├── ci-run.png            # CI success screenshot
│       └── docker-build.png      # Docker build screenshot
│
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── seed.py                      # Database population script
├── docker-compose.yml           # Multi-container orchestration
└── README.md                    # Sprint 1 documentation

```
## Tech Stack (Current – Sprint 1)
- Language: Python 3.11
- Framework: Flask
- Testing: pytest
- Database: PostgreSQL 15
- Security: Bcrypt (Password Hashing)
- CI: GitHub Actions
- Containerization: Docker

## Changes Made 
### Setup Application Skeleton & CI Pipeline Scope (Sprint 1 - Epic 1 (DEV))
The following items were completed in Sprint 1:
- Initialized Flask project structure
- Implemented basic application routes
- Created Dockerfile for containerization
- Configured GitHub Actions CI pipeline
- Verified application builds, tests run, and Docker image builds successfully

### Secure Database Design & Data Dictionary Implementation (Sprint 1 - Epic 2 (dev))
- Protected Credential Storage: Implemented Bcrypt hashing to ensure passwords are never stored in plain text.
- Data Isolation: Defined database schemas with NOT NULL constraints and Foreign Keys to enforce file ownership.
- Container Orchestration: Migrated to a multi-container setup (Flask + PostgreSQL) using Docker Compose.
- Database Health Checks: Implemented health checks and restart policies to handle service dependencies and prevent race conditions.
- Automated Seeding: Developed a seed.py script to populate the database with secure test data for CI validation.

## Data Dictionary (Database Schema)

The database layer enforces **Data Isolation** and **Protected Credential Storage** through strict integrity constraints to ensure system security.

### 1. Users Table
Stores authenticated entities and their security roles.

| Column | Data Type | Constraints | Security Purpose |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key | Unique internal identifier for the user. |
| `username` | String(80) | Unique, Not Null | Identity used for authentication; prevents account collisions. |
| `password_hash` | String(128) | Not Null | Stores salted **Bcrypt** hashes; ensures no plain text storage. |
| `role` | String(20) | Not Null | Defines access levels (e.g., 'admin', 'user') for Role-Based Access Control (RBAC). |

### 2. Files Table
Manages uploaded file metadata with mandatory ownership links.

| Column | Data Type | Constraints | Security Purpose |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key | Unique identifier for the file record. |
| `owner_id` | Integer | Foreign Key, Not Null | **Data Isolation**: Strictly binds every file to a valid user to prevent unauthorized access. |
| `original_filename`| String(255) | Not Null | Original filename for user-facing identification. |
| `stored_filename` | String(255) | Unique, Not Null | Randomized name on disk to prevent path traversal and filename guessing. |
| `size_bytes` | Integer | Not Null | Integrity check to verify the stored file size. |
| `created_at` | DateTime | Not Null | Audit trail for tracking data creation and file lifecycle. |


## Local Setup
### Start the entire infrastructure
```bash
docker compose up -d --build
```
### Remove Container (rebuild)
```bash
docker compose down
```
### Seed and Verify Security
```bash
# Populate the database
docker compose exec web python seed.py

# Verify Hashing (Audit Evidence)
docker exec -it app-db psql -U postgres -d appdb -c "SELECT username, password_hash FROM users;"
```
### Run Security Tests
```bash
docker compose exec web pytest -v.
```

Available endpoints:
- http://localhost:5000/
- http://localhost:5000/health
  
## CI Pipeline (github action) - workflow

**The CI pipeline is automatically triggered on:**
- Push to dev and main
- Pull requests targeting main

**Pipeline steps:** (Epic 1 Dev )
- Checkout source code
- Install Python dependencies
- Run automated tests
- Build Docker image

**Current Pipeline Steps (Epic 2 Dev Upgrade):**

- Source Checkout: Retrieves the latest code from the repository.
- Infrastructure Orchestration: Uses Docker Compose to launch both the Flask application and the PostgreSQL database.
- Health Monitoring: Implements a "wait-for-it" period to ensure the database is fully initialized before tests begin, preventing race conditions.
- Automated Security Seeding: Executes seed.py to populate the live database with test users and hashed credentials.
- Credential Audit: Prints hashed passwords to the CI logs, providing verifiable evidence that Bcrypt encryption is active.
- Security & Data Isolation Gates: Runs pytest inside the running container to verify that password hashing and file ownership constraints are strictly enforced.

## LLM Usage Declaration

### For Sprint 1 - Setup Application Skeleton & CI Pipeline Scope
**Tools used: ChatGPT (OpenAI)**

Example prompts:
- "Create a Flask project skeleton suitable for CI and Docker"
- "Explain the Flask app factory pattern"
- "Provide a minimal GitHub Actions workflow for pytest and Docker builds"

AI usage summary:
- AI tools were used as references to understand Flask project structuring,
CI pipeline configuration, and Docker setup.
- All suggested code and configurations were reviewed, adapted, and validated
locally and via GitHub Actions CI by the team.

### For Sprint 1 - Secure Database Design & Data Dictionary Implementation
Tools used: Gemini (Google)Example prompts:
- "Help me understand why the 'web' service crashes in CI while the 'db' service is still starting up."
- "How do I interpret a Bcrypt hash prefix like $2b$ to verify it meets security standards?"
- "Explain why my seed script is failing a 'NotNullViolation' when I've already defined the columns in SQLAlchemy."
- "What is the logic behind using Docker health checks for service dependency management?"
  
AI usage summary:Conceptual Learning: 
- AI was used to bridge the gap between application code and infrastructure.
- It helped me understand race conditions in container orchestration, leading to a more resilient setup using healthcheck and depends_on logic.
- Security Logic: Instead of just providing code, the AI acted as a tutor to explain the mechanics of Bcrypt, allowing me to verify Protected Credential Storage by auditing hashes directly in the database logs.
- Troubleshooting & Integrity: The AI helped me decode complex SQL error messages to learn how database constraints (like NOT NULL) enforce Data Isolation and prevent the insertion of incomplete, insecure records.
- Validation: All conceptual advice was translated into project-specific configurations, which I then manually validated through the CI pipeline and SQL terminal queries to ensure compliance with Epic 2 requirements

QA test trigger - Jan 17
