import logging
import socket


class Server:
    BUF_SIZE = 2048

    server_port = int
    server_socket = socket

    def __init__(self, server_port):
        self.server_port = server_port


class UDPServer(Server):

    def __init__(self, server_port):
        super().__init__(server_port)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', self.server_port))
        logging.info(' UDPServer: Server socket open with port ' + str(self.server_port))

        while True:
            recv_message, client_address = self.server_socket.recvfrom(Server.BUF_SIZE)
            logging.info(' UDPServer: Receive msg from client')

            send_msg = bytes(client_address[0] + ':' + str(client_address[1]), 'UTF-8')
            self.server_socket.sendto(send_msg, client_address)
            logging.info(' UDPServer: Send msg to client')


class TCPServer(Server):
    def __init__(self, server_port):
        super().__init__(server_port)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', self.server_port))
        self.server_socket.listen(1)
        logging.info(' TCPServer: Server socket open with port' +
                     ' ' +  str(self.server_port))

        while True:
            connection_socket, client_addr = self.server_socket.accept()
            str_client_addr = client_addr[0] + ':' + str(client_addr[1])
            logging.info(' TCPServer: Accept connection with ip: ' +
                         str_client_addr)

            recv_msg = connection_socket.recv(Server.BUF_SIZE)
            logging.info(' TCPServer: Receive msg from client with ip: ' +
                         str_client_addr)

            connection_socket.send(bytes(str_client_addr, 'UTF-8'))
            logging.info(' TCPServer: Send msg to client with ip: ' +
                         str_client_addr)

            connection_socket.close()
            logging.info(' TCPServer: Close connection with ip: ' +
                         str_client_addr)
