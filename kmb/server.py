"""Server Classes and Methods"""

import logging
import socket

from abc import ABC, abstractmethod


class Server(ABC):
    """Base class for the server"""
    BUF_SIZE = 2048

    server_ip = 'localhost'
    server_port = 12000
    server_socket = None

    def __init__(self, server_port, server_ip):
        self.server_port = server_port
        self.server_ip = server_ip

    @abstractmethod
    def start(self):
        """Basic method for starting the server"""
        pass


class UDPServer(Server):
    """Server conforming to UDP protocol"""

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.server_socket.bind((self.server_ip, self.server_port))
            logging.info(' UDPServer: Server socket open with port %s',
                         str(self.server_port))

            while True:
                recv_message, client_address = self.server_socket.recvfrom(Server.BUF_SIZE)
                logging.info(' UDPServer: Receive message from client with ip: %s',
                             client_address[0])

                bytes_client_addr = bytes(client_address[0] + ':' +
                                          str(client_address[1]), 'UTF-8')

                self.server_socket.sendto(bytes_client_addr, client_address)
                logging.info(' UDPServer: Send message to client with ip: %s',
                             client_address[0])
        except KeyboardInterrupt:
            self.server_socket.close()
            logging.info(' UDPServer: Server socket closed')
            return


class TCPServer(Server):
    """Server conforming to TCP protocol"""
    TIME_OUT = 2

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.server_ip, self.server_port))
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

        except KeyboardInterrupt:
            self.server_socket.close()
            logging.info(' UDPServer: Server socket closed')
            return
