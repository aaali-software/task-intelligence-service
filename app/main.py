from fastapi import FastAPI

from app.api.v1.task_analysis_routes import router

app = FastAPI(
    title="Task Intelligence Service",
    version="0.1.0",
    description="Python FastAPI microservice for analyzing task data.",
)

app.include_router(router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "UP"}