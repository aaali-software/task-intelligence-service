from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    TaskAnalysisException,
)

async def task_analysis_exception_handler(
    request: Request,
    exc: TaskAnalysisException,
): 
    return JSONResponse(
        status_code=400,
        content={
            "message": str(exc)
        },
    )
