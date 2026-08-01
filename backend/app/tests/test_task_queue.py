from app.services.task_queue import TaskQueueManager, TaskState


def test_task_queue_lifecycle():
    manager = TaskQueueManager()
    task = manager.enqueue("PDF_GEN", {"resume_id": 1})
    assert task.state == TaskState.PENDING

    # Execute dummy task
    def dummy_job():
        return "SUCCESS"

    result = manager.execute_task(task.job_id, dummy_job)
    assert result["state"] == TaskState.COMPLETED
    assert result["result"] == "SUCCESS"


def test_task_queue_cancellation():
    manager = TaskQueueManager()
    task = manager.enqueue("EMBED_GEN", {"chunks": []})
    cancelled = manager.cancel_task(task.job_id)
    assert cancelled is True
    assert manager.get_status(task.job_id)["state"] == TaskState.CANCELLED


def test_task_queue_retry():
    manager = TaskQueueManager()
    task = manager.enqueue("FAIL_JOB", {}, max_retries=1)

    attempt = 0

    def failing_job():
        nonlocal attempt
        attempt += 1
        if attempt == 1:
            raise ValueError("Temporary failure")
        return "RECOVERED"

    res = manager.execute_task(task.job_id, failing_job)
    assert res["state"] == TaskState.COMPLETED
    assert res["result"] == "RECOVERED"
