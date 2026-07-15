from enum import Enum

class NavigationResult(str, Enum):

    NEXT = "NEXT"
    REVIEW = "REVIEW"
    SUBMIT = "SUBMIT"
    SUCCESS = "SUCCESS"
    WAITING_USER = "WAITING_USER"
    NO_ACTION = "NO_ACTION"