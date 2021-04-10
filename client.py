"""Client Classes and Methods"""

import socket
import logging

from abc import ABC, abstractmethod


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
