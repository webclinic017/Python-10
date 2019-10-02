# python echoServer.py --port=8080
import sys
import socket
import argparse

host = 'localhost'
# 버퍼사이즈
data_payload = 2048
backlog =5
def echo_server(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    
    server_address = (host,port)
    print("Starting up echo server on %s port %s" %server_address)
    # Bind
    sock.bind(server_address)
    # Listen
    sock.listen(backlog)
    while True:
        print("Waiting to receive message from client ...")
        # return (hostaddr,port)
        client,address = sock.accept()        
        data = client.recv(data_payload)
        if data:
            print("Data: %s" %data)
            # data의 데이터 타입이 무엇일까?
            print("Data type: %s" %type(data))
            client.send(data)
            print("sent %s bytes back to %s" %(data,address))
            client.close()
if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Socket Server Example")
    parser.add_argument('--port',action="store",dest="port",type=int,required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
