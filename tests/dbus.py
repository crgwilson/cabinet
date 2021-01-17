from typing import Callable, Dict, List

import dbus


class MockDbusObject(object):
    def __init__(self, name: str, obj_methods: Dict[str, Callable]) -> None:
        self.name = name
        self.methods = {}

        for method_name, method in obj_methods.items():
            self.methods[method_name] = method

    def get_dbus_method(self, method: str, interface: str) -> Callable:
        return self.methods[method]


class MockDbusService(object):
    def __init__(self, name: str, objects: List[MockDbusObject]) -> None:
        self.name = name
        self.objects = {}

        for obj in objects:
            self.objects[obj.name] = obj

    def get_object(self, object: str) -> MockDbusObject:
        return self.objects[object]


class MockDbus(object):
    def __init__(self, services: List[MockDbusService]) -> None:
        self.services = {}

        for service in services:
            self.services[service.name] = service

    def get_object(self, service: str, object: str) -> MockDbusObject:
        service = self.services[service]

        return service.get_object(object)


def mock_show_exports() -> dbus.Struct:
    time_struct = dbus.Struct(
        (dbus.UInt64(1234567), dbus.UInt64(7654321)), signature=None
    )
    export_struct = dbus.Struct(
        (
            dbus.UInt16(0),
            dbus.String(u"/"),
            dbus.Boolean(False),
            dbus.Boolean(False),
            dbus.Boolean(False),
            dbus.Boolean(False),
            dbus.Boolean(False),
            dbus.Boolean(False),
            dbus.Boolean(False),
            dbus.Boolean(False),
            dbus.Struct(
                (dbus.UInt64(1610912783), dbus.UInt64(467767177)), signature=None
            ),
        ),
        signature=None,
    )

    val = dbus.Struct(
        (
            time_struct,
            dbus.Array([export_struct], signature=dbus.Signature("(qsbbbbbbbb(tt))")),
        )
    )
    return val
