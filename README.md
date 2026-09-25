# DevOps Task API

A Flask REST API created for the SIT223/SIT753 7.3HD Jenkins DevOps pipeline task.

## Features

- Health endpoint
- Task CRUD API
- SQLite persistence
- Automated Pytest tests
- Coverage reporting
- Docker containerisation
- Jenkins CI/CD pipeline
- SonarQube-ready configuration
- Trivy-ready security scanning
- Prometheus/Grafana monitoring configuration

## Local run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
flask --app app run --debug
```

Open http://localhost:5000/health

## Tests

```bash
pytest -q --cov=app --cov-report=xml
```

## Docker

```bash
docker compose up --build
```

## Jenkins stages

1. Build
2. Test
3. Code Quality
4. Security
5. Deploy
6. Release
7. Monitoring
