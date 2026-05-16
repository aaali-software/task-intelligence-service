# Task Intelligence Service

Small service for analyzing task lists and producing simple recommendations.

## Running tests

Use the included test wrappers to ensure the repository's Python environment is used.

PowerShell (Windows):

```powershell
.\scripts\run_tests.ps1
```

Bash (macOS/Linux):

```bash
./scripts/run_tests.sh
```

Run a single test file:

```powershell
.\scripts\run_tests.ps1 tests/test_task_analysis_service.py
```

Continuous Integration:

Tests run automatically on push and pull requests via GitHub Actions workflow at `.github/workflows/ci.yml`.

## Quickstart

Install dependencies into a virtual environment and run the service locally.

Create and activate a venv (Windows PowerShell):

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Run the FastAPI app (development):

```bash
python -m uvicorn app.main:app --reload
```

API endpoints:

- `GET /health` — basic health check

Testing and CI

- Use the scripts in `scripts/` to run tests with the repository Python interpreter.
- CI runs via `.github/workflows/ci.yml` on push/PR.

Contributing

- Open an issue or submit a PR. Keep changes focused and include tests.

License

- MIT License
See LICENSE file for details.
