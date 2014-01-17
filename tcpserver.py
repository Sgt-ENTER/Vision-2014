import socket
import threading
import time
import math
import SocketServer

counter = 0.0

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        global counter
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        x = math.sin(2.0*3.14159/100.0 * counter)
        y = math.cos(2.0*3.14159/100.0 * counter)
        w = 1.0 + math.sin(2.0*3.14159/50.0 * counter)
        counter += 1.0
        response = '{} {} {}'.format(x,y,w)
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "10.47.74.42", 4774

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    
    while True:
        # Infinite loop to keep the main thread running
        # and waiting for connections
        pass

