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

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

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
    due_soon_tasks: int
    high_priority_tasks: int
    completion_percentage: float
    productivity_score: int
    risk_level: RiskLevel
    priority_scores: list[TaskPriorityScore]
    top_focus_tasks: list[TaskPriorityScore]
    recommendations: list[str]

class TaskPriorityScore(BaseModel):
    task_id: int
    title: str
    priority_score: int
    reasons: list[str]