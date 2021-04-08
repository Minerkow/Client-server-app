import logging

import ParseInput
import Server
import Client

if __name__ == '__main__':
    session_parameters = ParseInput.parse_arguments()

    logging.basicConfig(filename=session_parameters.output_logs, filemode='w',
                        format='%(asctime)s %(name)s: %(levelname)s:%(message)s',
                        level=logging.INFO)

    if session_parameters.role == ParseInput.RoleParameters.SERVER:
        if (session_parameters.connectionParameters ==
                ParseInput.ConnectionParameters.UDP):
            server = Server.UDPServer(session_parameters.port)
            server.start()
        elif (session_parameters.connectionParameters ==
                ParseInput.ConnectionParameters.TCP):
            server = Server.TCPServer(session_parameters.port)
            server.start()
    elif session_parameters.role == ParseInput.RoleParameters.CLIENT:
        if (session_parameters.connectionParameters ==
                ParseInput.ConnectionParameters.UDP):
            client = Client.UDPClient(session_parameters.ip, session_parameters.port)
            client.start()
        elif (session_parameters.connectionParameters ==
                ParseInput.ConnectionParameters.TCP):
            client = Client.TCPClient(session_parameters.ip, session_parameters.port)
            client.start()



