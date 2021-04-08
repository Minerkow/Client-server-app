import logging
import socket

from abc import ABC, abstractmethod


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

    def __init__(self, server_port):
        super().__init__(server_port)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', self.server_port))
        logging.info(' UDPServer: Server socket open with port %s', str(self.server_port))

        while True:
            recv_message, client_address = self.server_socket.recvfrom(Server.BUF_SIZE)
            str_client_address = client_address[0] + ':' + str(client_address[1])
            logging.info(' UDPServer: Receive message from client with address: %s',
                         str_client_address)

            self.server_socket.sendto(bytes(str_client_address, 'UTF-8'),
                                      client_address)
            logging.info(' UDPServer: Send message to client with address: %s',
                         str_client_address)


class TCPServer(Server):
    TIME_OUT = 2

    def __init__(self, server_port):
        super().__init__(server_port)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))
        self.server_socket.listen(1)
        logging.info(' TCPServer: Server socket open with port: %s',
                     str(self.server_port))

        while True:
            connection_socket, client_addr = self.server_socket.accept()
            str_client_addr = client_addr[0] + ':' + str(client_addr[1])
            logging.info(' TCPServer: Accept connection with address: %s',
                         str_client_addr)

            try:
                connection_socket.settimeout(2)
                connection_socket.recv(Server.BUF_SIZE)
                logging.info(' TCPServer: Receive msg from client '
                             'with address: %s', str_client_addr)
            except socket.timeout:
                logging.error(' TCPServer: Message from client not received '
                              'with address %s, disconnection', str_client_addr)
                connection_socket.close()
                logging.info(' TCPServer: Close connection with address: %s',
                             str_client_addr)
                continue

            connection_socket.send(bytes(str_client_addr, 'UTF-8'))
            logging.info(' TCPServer: Send msg to client with address: %s',
                         str_client_addr)

            connection_socket.close()
            logging.info(' TCPServer: Close connection with address: %s',
                         str_client_addr)
