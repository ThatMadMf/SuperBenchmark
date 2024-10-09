from fastapi import FastAPI

from app import results, models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(results.router, prefix="/results/average")


@app.get("/live-feature")
async def live_feature():
    return {"message": "Live feature, works in both DEBUG and LIVE mode"}
