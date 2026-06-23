# points-mall-data

> Python FastAPI data service — implements a lightweight ETL pipeline that aggregates multi-source business data, cleans it, desensitizes sensitive fields, and exposes ready-to-render chart data and report exports for the admin dashboard.

## Responsibilities

- **ETL Scheduler** — `APScheduler` periodic job pulls raw data from Core, Shop, and Message services via BFF; stores normalized records in a local analytics schema
- **Data Cleaning** — remove null / invalid records, unify date formats to ISO 8601, normalize field names across heterogeneous service schemas
- **Sensitive Field Masking** — phone numbers, employee IDs, and names are desensitized before appearing in any exported report
- **Chart Data API** — REST endpoints returning time-series data for: attendance trend, daily points issuance, order volume, top redeemed products
- **Excel Report Export** — multi-sheet `.xlsx` workbook with Pandas + openpyxl: attendance sheet, points ledger sheet, orders sheet — all with masked PII
- **Data Dashboard Feed** — aggregated KPI metrics (total points issued, active employees, fulfillment rate) for the summary banner

## Why This Tech Stack

Data processing and analytics belong to Python. The ecosystem — Pandas, NumPy, openpyxl — has no equivalent in Java or Node.js for this class of work. FastAPI is chosen over Flask or Django because it is async-native (built on Starlette + uvicorn), which means the ETL HTTP calls to upstream services don't block each other. It also auto-generates interactive API docs from type annotations, matching the OpenAPI-first approach of the rest of the project.

Python 3.12 is used here for the `typing` improvements and the performance gains in the interpreter — meaningful when processing large attendance and points datasets.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Python 3.12, FastAPI 0.128 |
| ORM / DB | SQLAlchemy 2.x, PostgreSQL |
| Data Processing | Pandas, NumPy |
| Scheduling | APScheduler (in-process cron) |
| Excel Export | openpyxl |
| HTTP Client | httpx (async calls to BFF for data pull) |
| Auth | JWT middleware (validates BFF-issued tokens) |

## Docker

```bash
docker build -t points-mall-data .
docker run --env-file .env.dev -p 8083:8083 points-mall-data
```

## Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8083
# API:  http://localhost:8083
# Docs: http://localhost:8083/docs
```

## Docker

```bash
docker build -t points-mall-data .
docker run --env-file .env.dev -p 8083:8083 points-mall-data
```

## Key Environment Variables

```env
ENVIRONMENT=dev
DB_HOST=
DB_PORT=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_SSL_PARAMS=?sslmode=require
BFF_INTERNAL_URL=http://localhost:4000
```

## Code Quality

```bash
ruff check .            # Lint
ruff format --check .   # Check formatting
ruff format .           # Auto-fix formatting
```

Formatting and linting run automatically on staged `.py` files via the pre-commit hook. CI runs on every PR via `.github/workflows/ci.yml` in this repository.

## Design Note

This service covers the "lightweight ETL" tier — business data preprocessing that feeds a frontend dashboard. It is strictly separated from big-data infrastructure (no Spark, no Hive, no data warehouse). All transformations are pure Python, making the pipeline easy to reason about and modify.
