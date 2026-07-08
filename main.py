import os
import time
from datetime import datetime, timezone

from dotenv import load_dotenv

# Load profile-specific env file: .env.dev / .env.test / .env.prod
_env = os.getenv("ENVIRONMENT", "dev")
load_dotenv(f".env.{_env}", override=False)

from fastapi import FastAPI  # noqa: E402

app = FastAPI(title="Points Mall Data Service", version="0.1.0")

_start_time = time.time()


@app.get("/health")
def health():
    # Public route — no auth dependency
    return {
        "status": "ok",
        "service": "points-mall-data",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "db": "ok",
        "uptime": int(time.time() - _start_time),
    }


# All future business routes use: dependencies=[Depends(verify_token)]
# Example: @app.get("/reports", dependencies=[Depends(verify_token)])


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8083"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
