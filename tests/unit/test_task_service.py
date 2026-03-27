from unittest.mock import Mock

from schemas.tasks import TaskCreate
from services.tasks import TaskService


def test_create_task_calls_repository_and_returns_created_task():
    repository = Mock()
    service = TaskService(repository=repository)

    payload = TaskCreate(title="New Task", description="Task description", completed=False)
    created_task = Mock(id=1, title=payload.title, description=payload.description, completed=False, owner_id=42)
    repository.create.return_value = created_task

    result = service.create_task(task_in=payload, user_id=42)

    repository.create.assert_called_once_with(task_in=payload, user_id=42)
    assert result == created_task
