from fastapi import Depends

from core.exceptions import CommentNotFound, TaskNotFound
from models.comments import Comment
from repositories.comments import CommentRepository
from repositories.tasks import TaskRepository
from schemas.comments import CommentCreate


class CommentService:
    def __init__(
        self,
        comment_repository: CommentRepository = Depends(CommentRepository),
        task_repository: TaskRepository = Depends(TaskRepository),
    ):
        self.comment_repository = comment_repository
        self.task_repository = task_repository

    def create_comment(self, task_id: int, comment_in: CommentCreate, user_id: int) -> Comment:
        task = self.task_repository.get_by_id(task_id=task_id, user_id=user_id)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return self.comment_repository.create(task_id=task_id, user_id=user_id, comment_in=comment_in)

    def get_comments_by_task(self, task_id: int, user_id: int) -> list[Comment]:
        task = self.task_repository.get_by_id(task_id=task_id, user_id=user_id)
        if task is None:
            raise TaskNotFound(task_id=task_id)
        return self.comment_repository.get_by_task_id(task_id=task_id)

    def get_comment_by_id(self, task_id: int, comment_id: int, user_id: int) -> Comment:
        task = self.task_repository.get_by_id(task_id=task_id, user_id=user_id)
        if task is None:
            raise TaskNotFound(task_id=task_id)

        comment = self.comment_repository.get_by_id(comment_id=comment_id, task_id=task_id)
        if comment is None:
            raise CommentNotFound(comment_id=comment_id)
        return comment
