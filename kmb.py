"""
Melnikov Ignat 2021

This application is an implementation of simple client / server
application. For a detailed description of the commands,
call with the -h flag
"""
import argparse
import logging
import socket
import enum

from abc import ABC, abstractmethod


# -------------------------------Parse Input--------------------------------------------------


class ConnectionParameters(enum.Enum):
    """Connection parameters, possible connection protocols"""
    TCP = 1
    UDP = 2


class RoleParameters(enum.Enum):
    """Role parameters"""
    CLIENT = 1
    SERVER = 2


class SessionParameters:
    """Current session parameters"""
    port = int
    ip = str
    connection_parameters = ConnectionParameters
    role = RoleParameters
    output_logs = None

    def __init__(self, ip, port, connection_parameters, role, output_logs):
        self.port = port
        self.ip = ip
        self.connection_parameters = connection_parameters
        self.role = role
        self.output_logs = output_logs


def parse_arguments():
    """Parsing command line arguments for subtleties call with the -h flag"""
    parser = argparse.ArgumentParser("Connection and log saving parameters")
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
    group_logs_flags.add_argument("-f", help="Output of logs to file",
                                  type=str, default=None)

    args = parser.parse_args()

    type_connection = ConnectionParameters.UDP if args.u else ConnectionParameters.TCP
    role = RoleParameters.SERVER if args.s else RoleParameters.CLIENT
    output_logs = args.f

    return SessionParameters(args.host, args.port, type_connection, role, output_logs)


# -------------------------------Server--------------------------------------------------

class Server(ABC):
    """Base class for the server"""
    BUF_SIZE = 2048

    server_port = int
    server_socket = socket

    def __init__(self, server_port):
        self.server_port = server_port

    @abstractmethod
    def start(self):
        """Basic method for starting the server"""
        pass


class UDPServer(Server):
    """Server conforming to UDP protocol"""

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', self.server_port))
        logging.info(' UDPServer: Server socket open with port %s', str(self.server_port))

        while True:
            recv_message, client_address = self.server_socket.recvfrom(Server.BUF_SIZE)
            logging.info(' UDPServer: Receive message from client with ip: %s',
                         client_address[0])

            bytes_client_addr = bytes(client_address[0] + ':' +
                                      str(client_address[1]), 'UTF-8')

            self.server_socket.sendto(bytes_client_addr, client_address)
            logging.info(' UDPServer: Send message to client with ip: %s',
                         client_address[0])


class TCPServer(Server):
    """Server conforming to TCP protocol"""
    TIME_OUT = 2

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))
        self.server_socket.listen(1)
        logging.info(' TCPServer: Server socket open with port: %s',
                     str(self.server_port))

        while True:
            connection_socket, client_address = self.server_socket.accept()
            logging.info(' TCPServer: Accept connection with ip: %s',
                         client_address[0])

            try:
                connection_socket.settimeout(2)
                connection_socket.recv(Server.BUF_SIZE)
                logging.info(' TCPServer: Receive msg from client '
                             'with ip: %s', client_address[0])
            except socket.timeout:
                logging.error(' TCPServer: Message from client not received '
                              'with ip %s, disconnection', client_address[0])
                connection_socket.close()
                logging.info(' TCPServer: Close connection with ip: %s',
                             client_address[0])
                continue

            bytes_client_addr = bytes(client_address[0] + ':' +
                                      str(client_address[1]), 'UTF-8')
            connection_socket.send(bytes_client_addr)
            logging.info(' TCPServer: Send msg to client with ip: %s',
                         client_address[0])

            connection_socket.close()
            logging.info(' TCPServer: Close connection with ip: %s',
                         client_address[0])


# -------------------------------Client--------------------------------------------------

class Client(ABC):
    """Base class for the client"""

    BUF_SIZE = 2048

    server_ip = str
    server_port = int
    client_socket = socket

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    @abstractmethod
    def start(self):
        """Basic method for starting client"""
        pass


class UDPClient(Client):
    """Client requesting UDP"""
    TIME_OUT = 2

    def start(self):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logging.info(' UDPClient: Client socket open')

        hello_msg = bytes('Hello', 'UTF-8')
        self.client_socket.sendto(hello_msg, (self.server_ip, self.server_port))
        logging.info(' UDPClient: Sending message to server '
                     'with ip: %s', self.server_ip)

        try:
            self.client_socket.settimeout(UDPClient.TIME_OUT)
            recv_message, server_address = self.client_socket.recvfrom(Client.BUF_SIZE)
            logging.info(' UDPClient: Received reply message from the server '
                         'with ip: %s', self.server_ip)
            print(str(recv_message, 'UTF-8'))
        except socket.timeout:
            logging.error(' UDPClient: No response from the server has been '
                          'received within the allotted time')

        self.client_socket.close()
        logging.info(' UDPClient: Client socket closed')


class TCPClient(Client):
    """Client requesting TCP"""

    def start(self):

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
        except socket.error as err:
            logging.exception(err)
            self.client_socket.close()
            return

        logging.info(' TCPClient: Connect to server with ip: %s',
                     self.server_ip)

        hello_msg = bytes('Hello', 'UTF-8')
        self.client_socket.send(hello_msg)
        logging.info(' TCPClient: Sending a message to server '
                     'with ip: %s', self.server_ip)

        recv_msg = self.client_socket.recv(Client.BUF_SIZE)
        logging.info(' TCPClient: Received a reply message from the server '
                     'with ip: %s', self.server_ip)
        print(str(recv_msg, 'UTF-8'))

        self.client_socket.close()
        logging.info(' TCPClient: Client socket closed')


# -------------------------------Main--------------------------------------------------

if __name__ == '__main__':
    session_parameters = parse_arguments()

    logging.basicConfig(filename=session_parameters.output_logs, filemode='w',
                        format='%(asctime)s %(name)s: %(levelname)s:%(message)s',
                        level=logging.INFO)

    if session_parameters.role == RoleParameters.SERVER:
        if (session_parameters.connection_parameters ==
                ConnectionParameters.UDP):
            server = UDPServer(session_parameters.port)
            server.start()
        elif (session_parameters.connection_parameters ==
              ConnectionParameters.TCP):
            server = TCPServer(session_parameters.port)
            server.start()
    elif session_parameters.role == RoleParameters.CLIENT:
        if (session_parameters.connection_parameters ==
                ConnectionParameters.UDP):
            client = UDPClient(session_parameters.ip, session_parameters.port)
            client.start()
        elif (session_parameters.connection_parameters ==
              ConnectionParameters.TCP):
            client = TCPClient(session_parameters.ip, session_parameters.port)
            client.start()
