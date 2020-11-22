from typing import Any, List, Union

from flask_sqlalchemy.model import DefaultMeta

from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.sql.schema import Column

from cabinet.extensions import db


def session() -> scoped_session:
    return db.session


def commit() -> None:
    s = session()
    s.commit()


def refresh(model: DefaultMeta) -> None:
    s = session()
    s.refresh(model)


def get_model_column(model: DefaultMeta, column: str) -> Column:
    model_column = model.__table__.columns._data.get(column, None)
    if model_column is None:
        raise ValueError(model_column)

    return model_column


def get(model: DefaultMeta, value: Union[int, str], column: str = "id") -> DefaultMeta:
    result = model.query.filter(get_model_column(model, column) == value).first()
    return result


def get_list(model: DefaultMeta, value: Union[int, str], column: str = "id") -> Any:
    return model.query.filter(get_model_column(model, column) == value).all()


def get_all(model: DefaultMeta) -> List[Any]:
    results: List[DefaultMeta] = model.query.all()
    return results


def insert(model: DefaultMeta) -> DefaultMeta:
    s = session()
    s.add(model)
    commit()

    refresh(model)

    return model


def update(model: DefaultMeta) -> DefaultMeta:
    commit()
    refresh(model)

    return model


def delete(model: DefaultMeta) -> None:
    s = session()
    s.delete(model)
    commit()
