from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskRequest(BaseModel):
    id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None = None


class TaskAnalysisRequest(BaseModel):
    tasks: list[TaskRequest]


class TaskAnalysisResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    high_priority_tasks: int
    recommendations: list[str]