import argparse
import enum


class ConnectionParameters(enum.Enum):
    TCP = 1
    UDP = 2


class RoleParameters(enum.Enum):
    CLIENT = 1
    SERVER = 2


class SessionParameters:
    port = int
    ip = str
    connectionParameters = ConnectionParameters
    role = RoleParameters

    def __init__(self, port, ip, connection_parameters, role):
        self.port = port
        self.ip = ip
        self.connectionParameters = connection_parameters
        self.role = role


def parse_arguments():
    parser = argparse.ArgumentParser("Connection Argument Parser")
    group = parser.add_mutually_exclusive_group(required=False)

    parser.add_argument("host", help="Server ip address", type=str)
    parser.add_argument("port", help="Port for connection", type=int)
    parser.add_argument("-s", help="Start Server", action="store_true")
    parser.set_defaults(s=False)

    group.add_argument("-t", help="TCP mode", action="store_true")
    group.add_argument("-u", help="UDP mode", action="store_true")
    group.set_defaults(t=True, u=False)

    args = parser.parse_args()

    type_connection = ConnectionParameters.UDP if args.u else ConnectionParameters.TCP
    role = RoleParameters.SERVER if args.s else RoleParameters.CLIENT
    return SessionParameters(args.host, args.port, type_connection, role)
