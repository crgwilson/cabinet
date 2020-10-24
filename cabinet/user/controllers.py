from typing import List

from cabinet import database
from cabinet._types import ApiObjectAttribute
from cabinet.user.models import User


def get_all_users() -> List[User]:
    return database.get_all(User)


def get_user(user_id: int) -> User:
    return database.get(User, user_id)


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
