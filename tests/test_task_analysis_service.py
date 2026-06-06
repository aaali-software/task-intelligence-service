from datetime import UTC, datetime, timedelta
from urllib import response
import pytest

from app.models.task_models import (
    TaskAnalysisRequest,
    TaskPriority,
    TaskRequest,
    TaskStatus,
)
from app.services.task_analysis_service import (
    TaskAnalysisService,
    RiskLevel,
)

from app.exceptions.task_exceptions import (
    TaskAnalysisException,
)


def test_should_analyze_tasks_correctly():

    overdue_date = datetime.now(UTC) - timedelta(days=1)

    tasks = [
        TaskRequest(
            id=1,
            title="Overdue Task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH,
            due_date=overdue_date,
        ),
        TaskRequest(
            id=2,
            title="Completed Task",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.MEDIUM,
        ),
    ]

    request = TaskAnalysisRequest(tasks=tasks)

    response = TaskAnalysisService.analyze_tasks(request)

    assert response.total_tasks == 2
    assert response.completed_tasks == 1
    assert response.pending_tasks == 1
    assert response.overdue_tasks == 1
    assert response.due_soon_tasks == 0
    assert response.high_priority_tasks == 1
    assert response.productivity_score == 40

    assert (
        "Focus on overdue tasks first."
        in response.recommendations
    )

    assert len(response.priority_scores) == 2

    overdue_score = response.priority_scores[0]
    assert overdue_score.task_id == 1
    assert overdue_score.priority_score == 70
    assert "High priority" in overdue_score.reasons
    assert "Task overdue" in overdue_score.reasons

    assert response.completion_percentage == 50.0
    assert response.risk_level == RiskLevel.MEDIUM

    assert len(response.top_focus_tasks) == 2
    assert response.top_focus_tasks[0].task_id == 1

def test_should_throw_exception_when_task_list_is_empty():

    request = TaskAnalysisRequest(
        tasks=[]
    )

    with pytest.raises(
        TaskAnalysisException
        ):
            TaskAnalysisService.analyze_tasks(
                request
            )
