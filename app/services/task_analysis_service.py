from datetime import datetime, UTC

from app.models.task_models import (
    TaskAnalysisRequest,
    TaskAnalysisResponse,
    TaskStatus,
)


class TaskAnalysisService:

    @staticmethod
    def analyze_tasks(
        request: TaskAnalysisRequest,
    ) -> TaskAnalysisResponse:

        tasks = request.tasks

        total_tasks = len(tasks)

        completed_tasks = sum(
            1
            for task in tasks
            if task.status == TaskStatus.COMPLETED
        )

        pending_tasks = sum(
            1
            for task in tasks
            if task.status != TaskStatus.COMPLETED
        )

        overdue_tasks = sum(
            1
            for task in tasks
            if task.due_date
            and task.due_date < datetime.now(UTC)
            and task.status != TaskStatus.COMPLETED
        )

        high_priority_tasks = sum(
            1
            for task in tasks
            if task.priority.value == "HIGH"
        )

        recommendations = []

        if overdue_tasks > 0:
            recommendations.append(
                "Focus on overdue tasks first."
            )

        if high_priority_tasks > 3:
            recommendations.append(
                "You have many high priority tasks. Consider reprioritizing."
            )

        if completed_tasks == total_tasks and total_tasks > 0:
            recommendations.append(
                "Great job completing all tasks."
            )

        return TaskAnalysisResponse(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            overdue_tasks=overdue_tasks,
            high_priority_tasks=high_priority_tasks,
            recommendations=recommendations,
        )