import argparse
import enum
import sys


class ConnectionParameters(enum.Enum):
    TCP = 1
    UDP = 2


class RoleParameters(enum.Enum):
    CLIENT = 1
    SERVER = 2


class SessionParameters:
    port = int
    ip = str
    connection_parameters = ConnectionParameters
    role = RoleParameters
    output_logs = None

    def __init__(self, ip, port, connection_parameters, role, output_logs):
        self.port = port
        self.ip = ip
        self.connectionParameters = connection_parameters
        self.role = role
        self.output_logs = output_logs


def parse_arguments():
    parser = argparse.ArgumentParser("Connection Argument Parser")
    group_connection_flags = parser.add_mutually_exclusive_group(required=False)
    group_logs_flags = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument("host", help="Server ip address", type=str)
    parser.add_argument("port", help="Port for connection", type=int)
    parser.add_argument("-s", help="Start Server", action="store_true")
    parser.set_defaults(s=False)

    group_connection_flags.add_argument("-t", help="TCP mode", action="store_true")
    group_connection_flags.add_argument("-u", help="UDP mode", action="store_true")
    group_connection_flags.set_defaults(t=True, u=False)

    group_logs_flags.add_argument("-o", help="Output of logs to stdout",
                                  action="store_true")
    group_logs_flags.add_argument("-f", help="output of logs to file",
                                  type=str, default=None)

    args = parser.parse_args()

    type_connection = ConnectionParameters.UDP if args.u else ConnectionParameters.TCP
    role = RoleParameters.SERVER if args.s else RoleParameters.CLIENT
    output_logs = args.f

    return SessionParameters(args.host, args.port, type_connection, role, output_logs)
