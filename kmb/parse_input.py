"""
Functions and classes for processing and saving parameters of
current session
"""
import argparse
import enum

from dataclasses import dataclass


class ConnectionParameters(enum.Enum):
    """Connection parameters, possible connection protocols"""
    TCP = 1
    UDP = 2


class RoleParameters(enum.Enum):
    """Role parameters"""
    CLIENT = 1
    SERVER = 2


@dataclass
class SessionParameters:
    """Current session parameters"""
    port: int
    ip: str
    connection_parameters: ConnectionParameters
    role: RoleParameters
    output_logs: str


def parse_arguments():
    """Parsing command line arguments for subtleties call with the -h flag"""
    parser = argparse.ArgumentParser("Connection and log saving parameters")
    group_connection_flags = parser.add_mutually_exclusive_group(required=False)
    group_logs_flags = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument("host", help="Server ip address", type=str)
    parser.add_argument("port", help="Port for connection", type=int)
    parser.add_argument("-s", help="Start Server", action="store_true", default=False)

    group_connection_flags.add_argument("-t", help="TCP mode", action="store_true",
                                        default=True)
    group_connection_flags.add_argument("-u", help="UDP mode", action="store_true",
                                        default=False)

    group_logs_flags.add_argument("-o", help="Output of logs to stdout",
                                  action="store_true")
    group_logs_flags.add_argument("-f", help="Output of logs to file",
                                  type=str, default=None)

    args = parser.parse_args()

    type_connection = ConnectionParameters.UDP if args.u else ConnectionParameters.TCP
    role = RoleParameters.SERVER if args.s else RoleParameters.CLIENT
    output_logs = args.f

    return SessionParameters(args.port, args.host, type_connection, role, output_logs)
