import random
import string
from abc import ABC, abstractmethod
from typing import NoReturn

from cabinet import database
from cabinet.user.models import User


class BaseFactory(ABC):
    @staticmethod
    def create(model):
        return database.insert(model)

    @staticmethod
    def create_random_string(length: int = 5) -> str:
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))  # noqa: S311

    @abstractmethod
    def new(self) -> NoReturn:
        raise NotImplementedError()


class UserFactory(BaseFactory):
    def new(self) -> User:
        return self.create(
            User(
                username=self.create_random_string(),
                password=self.create_random_string(length=15),
            )
        )
