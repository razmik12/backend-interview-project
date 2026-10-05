from enum import Enum


class Prefix(str, Enum):
    PROJECT = "project"
    USER = "user"
    TASK = "task"
    PROJECT_MEMBER = "project_member"
    RATE_LIMIT = "rate_limit"
    LOCK = "lock"