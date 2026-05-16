from fastapi import APIRouter

from app.models.task_models import (
    TaskAnalysisRequest,
    TaskAnalysisResponse,
)
from app.services.task_analysis_service import (
    TaskAnalysisService,
)

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Task Analysis"],
)


@router.post(
    "/analyze",
    response_model=TaskAnalysisResponse,
)
def analyze_tasks(
    request: TaskAnalysisRequest,
) -> TaskAnalysisResponse:

    return TaskAnalysisService.analyze_tasks(request)