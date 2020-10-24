import typing

ApiObjectAttribute = typing.Union[str, int]
ApiObject = typing.Mapping[str, ApiObjectAttribute]

ApiResponse = typing.Tuple[ApiObject, int]
