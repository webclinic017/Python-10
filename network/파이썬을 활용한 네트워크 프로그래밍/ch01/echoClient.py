# python echoClient.py --port=8080

import socket
import sys
import argparse
host = 'localhost'

def echo_client(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (host,port)
    print("Connecting to %s port %s" %server_address)
    sock.connect(server_address)

    #send Data
    try:
        message = "Test message. This will be echoed"
        print("Sending %s" %message)
        sock.sendall(message.encode())
        # Look for the response
        amt_received = 0
        amt_expected = len(message)
        while amt_received < amt_expected:
            data=sock.recv(2048)
            amt_received+=len(data)
            print("Received: %s" %data)
    except socket.errno as e:
        print("Socket error: ",e)
    except Exception as e:
        print("Other error: ", e)
    finally:
        print("Closing connection to the server")
        sock.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Socket Server Example")
    parser.add_argument('--port',action="store",dest="port",type=int,required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)
        


# Traceback (most recent call last):
#   File "echoClient.py", line 16, in echo_client
#     sock.sendall(message)
# TypeError: a bytes-like object is required, not 'str'

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "echoClient.py", line 37, in <module>
#     echo_client(port)
#   File "echoClient.py", line 24, in echo_client
#     except socket.errno as e:
# TypeError: catching classes that do not inherit from BaseException is not allowed

