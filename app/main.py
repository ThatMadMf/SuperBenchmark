from typing import Dict

from fastapi import FastAPI

from app import results
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(results.router, prefix="/results/average")


@app.get("/live-feature", response_model=None)
async def live_feature() -> Dict[str, str]:
    return {"message": "Live feature, works in both DEBUG and LIVE mode"}
