from datetime import UTC, datetime, timedelta

from app.models.task_models import (
    RiskLevel,
    TaskAnalysisRequest,
    TaskAnalysisResponse,
    TaskPriority,
    TaskPriorityScore,
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

        completion_percentage = TaskAnalysisService._calculate_completion_percentage(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
        )

        risk_level = TaskAnalysisService._calculate_risk_level(
            overdue_tasks=overdue_tasks,
        )

        priority_scores = [
            TaskAnalysisService._calculate_task_priority_score(task, now)
            for task in tasks
        ]

        top_focus_tasks = sorted(
            priority_scores,
            key=lambda task: task.priority_score,
            reverse=True,
        )[:5]

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
            priority_scores=priority_scores,
            recommendations=recommendations,
            completion_percentage=completion_percentage,
            risk_level=risk_level,
            top_focus_tasks=top_focus_tasks,
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
    
    @staticmethod
    def _calculate_task_priority_score(
        task,
        now: datetime,
    ) -> TaskPriorityScore:
        score = 0
        reasons = []

        if task.priority == TaskPriority.HIGH:
            score += 40
            reasons.append("High priority")
        elif task.priority == TaskPriority.MEDIUM:
            score += 20
            reasons.append("Medium priority")

        if task.due_date and task.status != TaskStatus.COMPLETED:
            if task.due_date < now:
                score += 30
                reasons.append("Task overdue")
            elif task.due_date <= now + timedelta(days=1):
                score += 20
                reasons.append("Due within 24 hours")
            elif task.due_date <= now + timedelta(days=3):
                score += 10
                reasons.append("Due within 3 days")

        if task.status == TaskStatus.IN_PROGRESS:
            score += 10
            reasons.append("Already in progress")

        return TaskPriorityScore(
            task_id=task.id,
            title=task.title,
            priority_score=max(0, min(100, score)),
            reasons=reasons,
        )
    
    @staticmethod
    def _calculate_completion_percentage(
        total_tasks: int,
        completed_tasks: int,
    ) -> float:
        if total_tasks == 0:
            return 0.0

        return round((completed_tasks / total_tasks) * 100, 1)

    @staticmethod
    def _calculate_risk_level(
        overdue_tasks: int,
    ) -> RiskLevel:
        if overdue_tasks == 0:
            return RiskLevel.LOW

        if overdue_tasks <= 2:
            return RiskLevel.MEDIUM

        if overdue_tasks <= 5:
            return RiskLevel.HIGH

        return RiskLevel.CRITICAL
