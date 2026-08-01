# Contributing to HireMind AI

Thank you for your interest in contributing to **HireMind AI**!

## Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/shambhushekharsinha-engg/HireMind-AI.git
   cd HireMind-AI
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv backend/venv
   source backend/venv/bin/activate  # On Windows: backend\venv\Scripts\activate
   pip install -r backend/requirements.txt pytest ruff black isort pre-commit
   ```

3. **Install Pre-Commit Hooks**:
   ```bash
   pre-commit install
   ```

4. **Run Database Migrations**:
   ```bash
   cd backend
   alembic upgrade head
   ```

## Code Quality Guidelines

- **Formatting & Linting**:
  - Run Black: `black backend/app`
  - Run Ruff: `ruff check backend/app`
  - Run isort: `isort backend/app`

- **Running Tests**:
  ```bash
  cd backend
  python -m pytest app/tests/ -v
  ```

- **Branch Naming & Pull Requests**:
  - Use descriptive branch names: `feature/repository-pattern`, `fix/ats-scorer`.
  - Ensure all CI/CD checks pass before submitting PRs.
