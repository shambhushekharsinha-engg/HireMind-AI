import uuid
import time
from typing import Dict, Any, Optional, Callable

class TaskState:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskItem:
    def __init__(self, task_type: str, payload: Dict[str, Any], max_retries: int = 3):
        self.job_id = f"job-{uuid.uuid4().hex[:10]}"
        self.task_type = task_type
        self.payload = payload
        self.state = TaskState.PENDING
        self.retries = 0
        self.max_retries = max_retries
        self.result = None
        self.error = None
        self.created_at = time.time()
        self.updated_at = time.time()

class TaskQueueManager:
    """
    Async Task Queue Manager with support for retries, cancellations, and state tracking:
    PENDING -> RUNNING -> RETRYING -> CANCELLED -> COMPLETED -> FAILED
    """
    def __init__(self):
        self.tasks: Dict[str, TaskItem] = {}

    def enqueue(self, task_type: str, payload: Dict[str, Any], max_retries: int = 3) -> TaskItem:
        task = TaskItem(task_type, payload, max_retries)
        self.tasks[task.job_id] = task
        return task

    def get_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        task = self.tasks.get(job_id)
        if not task:
            return None
        return {
            "job_id": task.job_id,
            "task_type": task.task_type,
            "state": task.state,
            "retries": task.retries,
            "result": task.result,
            "error": task.error
        }

    def cancel_task(self, job_id: str) -> bool:
        task = self.tasks.get(job_id)
        if not task:
            return False
        if task.state in [TaskState.PENDING, TaskState.RUNNING, TaskState.RETRYING]:
            task.state = TaskState.CANCELLED
            task.updated_at = time.time()
            return True
        return False

    def execute_task(self, job_id: str, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        task = self.tasks.get(job_id)
        if not task or task.state == TaskState.CANCELLED:
            return {"job_id": job_id, "state": TaskState.CANCELLED if task else "NOT_FOUND"}

        task.state = TaskState.RUNNING
        task.updated_at = time.time()

        try:
            res = func(*args, **kwargs)
            task.result = res
            task.state = TaskState.COMPLETED
        except Exception as e:
            if task.retries < task.max_retries:
                task.retries += 1
                task.state = TaskState.RETRYING
                return self.execute_task(job_id, func, *args, **kwargs)
            else:
                task.error = str(e)
                task.state = TaskState.FAILED

        task.updated_at = time.time()
        return self.get_status(job_id)

task_queue_manager = TaskQueueManager()
