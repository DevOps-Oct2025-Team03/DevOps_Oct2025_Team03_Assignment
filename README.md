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
│   └── test_basic.py            # Sanity test for CI
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
├── README.md                    # Sprint 1 documentation

```
## Tech Stack (Current – Sprint 1)
- Language: Python 3.11
- Framework: Flask
- Testing: pytest
- CI: GitHub Actions
- Containerization: Docker


## Setup Application Skeleton & CI Pipeline Scope (Sprint 1 - Epic 1 (DEV))
The following items were completed in Sprint 1:
- Initialized Flask project structure
- Implemented basic application routes
- Created Dockerfile for containerization
- Configured GitHub Actions CI pipeline
- Verified application builds, tests run, and Docker image builds successfully

## Run Locally 
```text
pip install -r requirements.txt
python run.py
```
Available endpoints:
- http://localhost:5000/
- http://localhost:5000/health

## Run Test 
```text
pytest -v
```
## Docker
**Build Docker Image**
```bash
docker build -t flask-devops-app .
```
**Run Docker Container**
```bash
docker run -p 5000:5000 flask-devops-app
```
## CI Pipeline (github action) - workflow

**The CI pipeline is automatically triggered on:**
- Push to dev and main
- Pull requests targeting main

**Pipeline steps:**
- Checkout source code
- Install Python dependencies
- Run automated tests
- Build Docker image

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

### For Sprint 1 - 
update all other LLM decalration here follow top format
