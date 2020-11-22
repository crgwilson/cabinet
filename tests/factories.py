import random
import string
from abc import ABC, abstractmethod
from typing import NoReturn, Optional

from cabinet import database
from cabinet.auth.controllers import AuthToken, get_role
from cabinet.auth.models import Session
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
    role_ids = []

    def new(self, password: Optional[str] = None) -> User:
        if not password:
            password = self.create_random_string(length=15)

        roles_to_add = []
        for role_id in self.role_ids:
            roles_to_add.append(get_role(role_id))

        return self.create(
            User(
                username=self.create_random_string(),
                password=password,
                roles=roles_to_add,
            )
        )


class AdminUserFactory(UserFactory):
    role_ids = [1]


class SessionFactory(BaseFactory):
    def new(self, user_id: int, ttl: int = 600) -> Session:
        return self.create(Session(user_id=user_id, ttl=ttl))


class SessionTokenFactory(BaseFactory):
    def new(self, session: Session, secret: str) -> bytes:
        token = AuthToken(
            user_id=session.user_id,
            created_on=session.created_on,
            ttl=session.ttl,
            secret=secret,
        )
        return token.encode()
