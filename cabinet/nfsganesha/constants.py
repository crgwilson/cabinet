from typing import NamedTuple


class NfsGaneshaConstants(NamedTuple):
    SERVICE = "org.ganesha.nfsd"

    EXPORT_MANAGER_INTERFACE = SERVICE + ".exportmgr"
    EXPORT_MANAGER_OBJECT = "/org/ganesha/nfsd/ExportMgr"

    EXPORT_MANAGER_ADD_EXPORT_METHOD = "AddExport"
    EXPORT_MANAGER_REMOVE_EXPORT_METHOD = "RemoveExport"
    EXPORT_MANAGER_UPDATE_EXPORT_METHOD = "UpdateExport"
    EXPORT_MANAGER_DISPLAY_EXPORT_METHOD = "DisplayExport"
    EXPORT_MANAGER_SHOW_EXPORTS_METHOD = "ShowExports"

    EXPORT_MANAGER_METHODS = [
        EXPORT_MANAGER_ADD_EXPORT_METHOD,
        EXPORT_MANAGER_REMOVE_EXPORT_METHOD,
        EXPORT_MANAGER_UPDATE_EXPORT_METHOD,
        EXPORT_MANAGER_DISPLAY_EXPORT_METHOD,
        EXPORT_MANAGER_SHOW_EXPORTS_METHOD,
    ]


nfs_ganesha_constants = NfsGaneshaConstants()
