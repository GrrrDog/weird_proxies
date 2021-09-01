import socket
import threading
import re

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  

print('Listening on {}:{}'.format(bind_ip, bind_port))

def handle_client_connection(client_socket):
    request = client_socket.recv(8192)

    print('Received:\n>>{}'.format(request))
    test_id = b'xxx'
    test_id_pattern = b'testid'
    decodedReq = request.decode("ascii")
    p = re.compile("testhere(\d+)idhere", re.MULTILINE)
    result = p.search(decodedReq)
    if result:
        test_id = bytes(result[1], 'ascii')

    body = b'1234567890.testid=' + test_id + b'\r\n'
    body = body + request
    body = body + b'0987654321.testid=' + test_id + b'\r\n'
    resp = b'HTTP/1.1 200 OK\r\nContent-Length: ' + \
           str.encode(str(len(body))) + b'\r\nConnection: Closed\r\n\r\n' + body
    client_socket.send(resp)
    print("<<", end ="")
    print(resp)
    client_socket.close()


while True:
    client_sock, address = server.accept()
    # print 'Accepted connection from {}:{}'.format(address[0], address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()
