# points-mall-data

> Python FastAPI data service — implements a lightweight ETL pipeline that aggregates multi-source business data, cleans it, desensitizes sensitive fields, and exposes ready-to-render chart data and report exports for the admin dashboard.

## Responsibilities

- **ETL Scheduler** — `APScheduler` periodic job pulls raw data from Core, Shop, and Message services via BFF; stores normalized records in a local analytics schema
- **Data Cleaning** — remove null / invalid records, unify date formats to ISO 8601, normalize field names across heterogeneous service schemas
- **Sensitive Field Masking** — phone numbers, employee IDs, and names are desensitized before appearing in any exported report
- **Chart Data API** — REST endpoints returning time-series data for: attendance trend, daily points issuance, order volume, top redeemed products
- **Excel Report Export** — multi-sheet `.xlsx` workbook with Pandas + openpyxl: attendance sheet, points ledger sheet, orders sheet — all with masked PII
- **Data Dashboard Feed** — aggregated KPI metrics (total points issued, active employees, fulfillment rate) for the summary banner

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Python 3.11, FastAPI |
| ORM / DB | SQLAlchemy 2.x, PostgreSQL |
| Data Processing | Pandas, NumPy |
| Scheduling | APScheduler (in-process cron) |
| Excel Export | openpyxl |
| HTTP Client | httpx (async calls to BFF for data pull) |
| Auth | JWT middleware (validates BFF-issued tokens) |

## Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8083
# API:  http://localhost:8083
# Docs: http://localhost:8083/docs
```

## Key Environment Variables

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/points_data
BFF_BASE_URL=http://localhost:4000
BFF_INTERNAL_SECRET=shared-hmac-secret
ETL_SCHEDULE_CRON=0 2 * * *
```

## Design Note

This service covers the "lightweight ETL" tier — business data preprocessing that feeds a frontend dashboard. It is strictly separated from big-data infrastructure (no Spark, no Hive, no data warehouse). All transformations are pure Python, making the pipeline easy to reason about and modify.
