# Client-server-app
Simple client-server application by Melnikov Ignat

###### Start

python -m kmb <flags> 

###### Arguments
~~~~
 Connection and log saving parameters [-h] [-s] [-t | -u] (-o | -f F)
                                       
positional arguments:

  host        Server ip address

  port        Port for connection

optional arguments:
  -h, --help  show this help message and exit
  -s          Start Server
  -t          TCP mode
  -u          UDP mode
  -o          Output of logs to stdout
  -f <file>   Output of logs to file