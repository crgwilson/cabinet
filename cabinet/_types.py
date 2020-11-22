import typing

from flask_sqlalchemy.model import DefaultMeta

QueryResult = typing.Union[typing.Dict[str, typing.Any], typing.List[DefaultMeta]]

ApiObjectAttribute = typing.Union[str, int]
ApiObject = typing.Mapping[str, ApiObjectAttribute]

ApiResponse = typing.Tuple[ApiObject, int]
