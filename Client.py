import socket
import logging


class Client:

    BUF_SIZE = 2048

    server_ip = str
    server_port = int
    client_socket = socket

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port


class UDPClient(Client):
    def __init__(self, server_ip, server_port):
        super().__init__(server_ip, server_port)

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logging.info('UDPClient: Client socket open')

        hello_msg = bytes('Hello', 'UTF-8')
        self.client_socket.sendto(hello_msg, (self.server_ip, self.server_port))
        logging.info('UDPClient: Msg sent to server')

        recv_message, server_address = self.client_socket.recvfrom(Client.BUF_SIZE)
        logging.info('UDPClient: Msg receive from server')

        print(str(recv_message, 'UTF-8'))
        self.client_socket.close()


