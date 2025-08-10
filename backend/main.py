from fastapi import FastAPI, HTTPException
from routes.analyze import router as analyze_router

app = FastAPI(title="FakeSaleFinder API")

@app.get("/api/health")
def health():
    return {"status":"ok"}

app.include_router(analyze_router, prefix="/api")
