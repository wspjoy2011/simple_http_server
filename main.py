import socket


def start_web_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 2000))
        server.listen(5)
        while True:
            print('Server waiting...')
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            content = load_page_from_get_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print('Shutdown server.')


def load_page_from_get_request(request):
    HEADERS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HEADERS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = request.split(' ')[1]
    if path == '/':
        print(path)
        path = '/home.html'
    response = ''
    try:
        with open('views' + path, 'rb') as file:
            response = file.read()
        return HEADERS.encode('utf-8') + response
    except FileNotFoundError:
        return (HEADERS + 'Sorry, page not found...').encode('utf-8')


if __name__ == '__main__':
    start_web_server()
