"""
Melnikov Ignat 2021

This application is an implementation of simple client / server
application. For a detailed description of the commands,
call with the -h flag
"""
import logging

from kmb import parse_input, server, client

if __name__ == '__main__':
    session_parameters = parse_input.parse_arguments()

    logging.basicConfig(filename=session_parameters.output_logs, filemode='w',
                        format='%(asctime)s %(name)s: %(levelname)s:%(message)s',
                        level=logging.INFO)

    if session_parameters.role == parse_input.RoleParameters.SERVER:
        if (session_parameters.connection_parameters ==
                parse_input.ConnectionParameters.UDP):
            server = server.UDPServer(session_parameters.port,
                                      session_parameters.ip)
            server.start()
        elif (session_parameters.connection_parameters ==
              parse_input.ConnectionParameters.TCP):
            server = server.TCPServer(session_parameters.port,
                                      session_parameters.ip)
            server.start()
    elif session_parameters.role == parse_input.RoleParameters.CLIENT:
        if (session_parameters.connection_parameters ==
                parse_input.ConnectionParameters.UDP):
            client = client.UDPClient(session_parameters.ip, session_parameters.port)
            client.start()
        elif (session_parameters.connection_parameters ==
              parse_input.ConnectionParameters.TCP):
            client = client.TCPClient(session_parameters.ip, session_parameters.port)
            client.start()
