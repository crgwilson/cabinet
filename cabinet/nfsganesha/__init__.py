from enum import Enum
from typing import List, Optional

import dbus

from flask import Flask


# class ExportAccessType(Enum):
#     NONE = "None"
#     RW = "RW"
#     RO = "RO"
#     MDONLY = "MDONLY"
#     MDONLY = "MDONLY_RO"
#
#
# class ExportProtocol(Enum):
#     NFSv3 = "3"
#     NFSv4 = "4"
#
#
# class ExportTransports(Enum):
#     TCP = "TCP"
#     UDP = "UDP"
#     RDMA = "RDMA"
#
#
# class ExportSecurityType(Enum):
#     NONE = "none"
#     # local unix uids and gids using AUTH_SYS
#     SYSTEM = "sys"
#     KRB5 = "krb5"
#     # kerberos v5 w/ integrity checking
#     KRB5I = "krb5i"
#     # kerberos v5 with integrity checking and encryption
#     KRB5P = "krb5p"
#
#
# class ExportSquash(Enum):
#     ROOT_SQUASH = "root_squash"
#     ROOT_ID_SQUASH = "root_id_squash"
#     ALL_SQUASH = "all_squash"
#     ALL_ANONYMOUS = "all_anonymous"
#     NONE = "none"
#
#
# class ExportDelegations(Enum):
#     READ = "read"
#     WRITE = "write"
#     READ_AND_WRITE = "readwrite"
#     NONE = "None"
#
#
# class NfsGaneshaExportDefaults(object):
#     def __init__(
#         self,
#         access_type: ExportAccessType,
#         protocols: List[ExportProtocol],
#         transports: List[ExportTransports],
#         anonymous_uid: int,
#         anonymous_gid: int,
#         sec_type: List[ExportSecurityType],
#         privileged_port: bool,
#         manage_gids: bool,
#         squash: ExportSquash,
#         nfs_commit: bool,
#         delegations: ExportDelegations,
#         attr_expiration_time: int,
#     ):
#         pass
#
#
# class NfsGaneshaExport(object):
#     def __init__(
#         self,
#         id: int,
#         path: str,
#         pseudo: str,
#         fielsystem_id: int,
#     ):
#         pass
#
#
# class NfsGanesha(object):
#     GANESHA_SERVICE = "org.ganesha.nfsd"
#     GANESHA_EXPORT_MANAGER = "/org/ganesha/nfsd/ExportMgr"
#
#     def __init__(self, connection: Optional[dbus.SystemBus] = None):
#         if not connection:
#             connection = dbus.SystemBus()
#
#         self.conn = connection
#
#     def init_app(self, app: Flask):
#         if self.GANESHA_SERVICE not in self.connection.list_names:
#             raise RuntimeError("No nfs-ganesha dbus service available")
#
#     def add_export(self, config_path: str, search_expr: str):
#         pass
#
#     def remove_export(self, id: int):
#         pass
#
#     def update_export(self, config_path: str, search_expr: str):
#         pass
#
#     def display_export(self, id: int):
#         pass
#
#     def show_exports(self):
#         pass
