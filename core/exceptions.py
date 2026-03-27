class AppException(Exception):
    status_code = 400
    code = "APP_ERROR"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TaskNotFound(AppException):
    status_code = 404
    code = "TASK_NOT_FOUND"

    def __init__(self, task_id: int):
        super().__init__(message=f"Task with id={task_id} not found")


class CommentNotFound(AppException):
    status_code = 404
    code = "COMMENT_NOT_FOUND"

    def __init__(self, comment_id: int):
        super().__init__(message=f"Comment with id={comment_id} not found")
