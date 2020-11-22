from typing import List

from cabinet import database
from cabinet._types import ApiObjectAttribute
from cabinet.user.models import User


def get_all_users() -> List[User]:
    return database.get_all(User)


def get_user(user_id: int) -> User:
    return database.get(User, user_id)


def get_user_by_username(username: str) -> User:
    return database.get(User, username, column="username")


def create_user(**kwargs: ApiObjectAttribute) -> User:
    user = User(**kwargs)
    return database.insert(user)


def update_user(user_id: int, **kwargs: ApiObjectAttribute) -> User:
    user = get_user(user_id)
    user.username = kwargs["username"]
    # TODO change other stuff too
    return database.update(user)


def delete_user(user_id: int) -> None:
    user = get_user(user_id)
    database.delete(user)


def validate_user_credentials(username: str, password: str) -> bool:
    user = get_user_by_username(username)
    if not user:
        # user doesn't exist
        return False

    valid_password: bool = user.check_password(password)
    return valid_password
