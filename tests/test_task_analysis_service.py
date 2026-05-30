from datetime import UTC, datetime, timedelta
from urllib import response

from app.models.task_models import (
    TaskAnalysisRequest,
    TaskPriority,
    TaskRequest,
    TaskStatus,
)
from app.services.task_analysis_service import (
    TaskAnalysisService,
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