import socket
import threading
import SocketServer

from ball import BallFinder

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(8) # We only expect 1 byte, but be careful anyway
        # Determine what thread to use in order to get the data requested
        if data[0].lower() == 'g':
            # We want the goal tracking thread
            pass # TODO - remove when actual code is in place
            
        elif data[0].lower() == 'r' or data[0].lower() == 'b':
            # Catching thread
            pass # TODO - remove when actual code is in place
        
        else:
            response = '-999' # Invalid request
        
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "", 4774 # Bind to all address on port 4774

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever, name="tcpserver")
    # Exit the server thread when the main thread terminates
    # Makes breaking out of program with Ctrl-C easier
    server_thread.daemon = True
    server_thread.start()
    
    while True:
        # Infinite loop to keep the main thread running
        # and waiting for connections
        # Makes breaking out of program with Ctrl-C easier
        pass

