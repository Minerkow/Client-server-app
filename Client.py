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
        logging.info(' UDPClient: Client socket open')

        hello_msg = bytes('Hello', 'UTF-8')
        self.client_socket.sendto(hello_msg, (self.server_ip, self.server_port))
        logging.info(' UDPClient: Msg sent to server')

        recv_message, server_address = self.client_socket.recvfrom(Client.BUF_SIZE)
        logging.info(' UDPClient: Msg receive from server')

        print(str(recv_message, 'UTF-8'))
        self.client_socket.close()
        logging.info(' UDPClient: Client socket closed')


class TCPClient(Client):
    def __init__(self, server_ip, server_port):
        super().__init__(server_ip, server_port)

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        str_server_addr = self.server_ip + ':' + str(self.server_port)
        logging.info(' TCPClient: Connect with server with ip: ' +
                     str_server_addr)

        hello_msg = bytes('Hello', 'UTF-8')
        self.client_socket.send(hello_msg)
        logging.info(' TCPClient: Send msg to server with ip: ' +
                     str_server_addr)

        recv_msg = self.client_socket.recv(Client.BUF_SIZE)
        logging.info(' TCPClient: Receive msg from server with ip: ' +
                     str_server_addr)
        print(str(recv_msg, 'UTF-8'))

        self.client_socket.close()
        logging.info(' TCPClient: Client socket closed')




