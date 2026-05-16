from datetime import UTC, datetime, timedelta

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
        now = datetime.now(UTC)
        due_soon_cutoff = now + timedelta(days=3)

        total_tasks = len(tasks)

        completed_tasks = sum(
            1 for task in tasks
            if task.status == TaskStatus.COMPLETED
        )

        pending_tasks = sum(
            1 for task in tasks
            if task.status != TaskStatus.COMPLETED
        )

        overdue_tasks = sum(
            1 for task in tasks
            if task.due_date
            and task.due_date < now
            and task.status != TaskStatus.COMPLETED
        )

        due_soon_tasks = sum(
            1 for task in tasks
            if task.due_date
            and now <= task.due_date <= due_soon_cutoff
            and task.status != TaskStatus.COMPLETED
        )

        high_priority_tasks = sum(
            1 for task in tasks
            if task.priority.value == "HIGH"
        )

        productivity_score = TaskAnalysisService._calculate_productivity_score(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            overdue_tasks=overdue_tasks,
        )

        recommendations = []

        if overdue_tasks > 0:
            recommendations.append("Focus on overdue tasks first.")

        if due_soon_tasks > 0:
            recommendations.append("You have tasks due soon. Plan time for them.")

        if high_priority_tasks > 3:
            recommendations.append(
                "You have many high priority tasks. Consider reprioritizing."
            )

        if completed_tasks == total_tasks and total_tasks > 0:
            recommendations.append("Great job completing all tasks.")

        return TaskAnalysisResponse(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            overdue_tasks=overdue_tasks,
            due_soon_tasks=due_soon_tasks,
            high_priority_tasks=high_priority_tasks,
            productivity_score=productivity_score,
            recommendations=recommendations,
        )

    @staticmethod
    def _calculate_productivity_score(
        total_tasks: int,
        completed_tasks: int,
        overdue_tasks: int,
    ) -> int:
        if total_tasks == 0:
            return 100

        completion_rate = completed_tasks / total_tasks
        overdue_penalty = overdue_tasks * 10

        score = round((completion_rate * 100) - overdue_penalty)

        return max(0, min(100, score))