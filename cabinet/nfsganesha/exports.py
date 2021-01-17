from typing import List, Optional

import dbus

from cabinet.nfsganesha.constants import nfs_ganesha_constants


class Export(object):
    @classmethod
    def unpack(cls, dbus_struct: dbus.Struct) -> "Export":
        cls.id = dbus_struct[0]
        cls.path = dbus_struct[1]
        cls.nfsv3 = dbus_struct[2]
        cls.mnt = dbus_struct[3]
        cls.nlm4 = dbus_struct[4]
        cls.rquota = dbus_struct[5]
        cls.nfsv40 = dbus_struct[6]
        cls.nfsv41 = dbus_struct[7]
        cls.nfsv42 = dbus_struct[8]
        cls.nfs9p = dbus_struct[9]

        return cls


class ExportManager(object):
    DBUS_SERVICE_NAME = nfs_ganesha_constants.SERVICE
    DBUS_INTERFACE_NAME = nfs_ganesha_constants.EXPORT_MANAGER_INTERFACE
    DBUS_OBJECT_NAME = nfs_ganesha_constants.EXPORT_MANAGER_OBJECT
    DBUS_METHODS = nfs_ganesha_constants.EXPORT_MANAGER_METHODS

    # This type is probably wrong
    def __init__(self, connection: Optional[dbus.SystemBus] = None):
        self._dbus_obj = connection.get_object(
            self.DBUS_SERVICE_NAME, self.DBUS_OBJECT_NAME
        )

        self._dbus_methods = {}
        for method in self.DBUS_METHODS:
            self._dbus_methods[method] = self._dbus_obj.get_dbus_method(
                method,
                self.DBUS_INTERFACE_NAME,
            )

    def show_exports(self) -> List[Export]:
        _show_exports = self._dbus_methods[
            nfs_ganesha_constants.EXPORT_MANAGER_SHOW_EXPORTS_METHOD
        ]
        result = _show_exports()
        result_exports = result[1]

        output = []
        for export in result_exports:
            e = Export.unpack(export)
            output.append(e)

        return output
