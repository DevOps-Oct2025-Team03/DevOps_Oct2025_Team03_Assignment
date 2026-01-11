# Kanban Workflow & Process Rules

## Overview
This project adopts a Kanban-based workflow to manage the DevSecOps lifecycle.
The workflow ensures transparency, accountability, and quality gates across
development, testing, and deployment activities.

## Kanban Columns
- **Backlog**: Approved work items not yet started.
- **Ready**: Tasks with clearly defined objectives and acceptance criteria.
- **In Progress**: Tasks actively being worked on by team members.
- **PR Review**: Tasks completed and awaiting pull request review.
- **Testing / Security**: Automated testing and security scans are executed.
- **Done**: Tasks completed successfully with all checks passed.

## Work-In-Progress (WIP) Limits
To minimise bottlenecks and context switching:
- Each team member is limited to a maximum of **2 tasks** in the **In Progress** column.

## Task Flow
1. The Scrum Master creates tasks in the Backlog.
2. Tasks move to Ready once scope and acceptance criteria are finalised.
3. Team members pull tasks into In Progress.
4. Code changes are submitted via Pull Requests and tasks move to PR Review.
5. CI pipelines execute automated tests and security scans in Testing / Security.
6. Tasks move to Done only when all checks pass and evidence is captured.

## Definition of Done
A task is considered Done only when:
- Code is merged via Pull Request.
- CI pipeline passes successfully.
- Testing and security checks show no blocking issues.
- Required evidence is documented.
