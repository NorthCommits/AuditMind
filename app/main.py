from fastapi import FastAPI
from app.api import decisions_router


app = FastAPI(
    title="AuditMind",
    description="API-first Decision Audit and Explainability Platform",
    version="0.1.0"
)
app.include_router(decisions_router)



@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "auditmind",
        "version": "0.1.0"
    }
