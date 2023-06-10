import socket
import json
from datetime import datetime

TCP_PORT = 5000
BUFFER_SIZE = 1048576
LOG_FILE = 'chunk_upload_log.txt'

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', TCP_PORT)
    sock.bind(server_address)
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        try:
            data = connection.recv(BUFFER_SIZE)
            message = json.loads(data.decode('utf-8'))
            filename = message.get('requestedcontent', '')

            with open(filename, 'rb') as file_handle:
                chunk_data = file_handle.read()
                connection.sendall(chunk_data)

            with open(LOG_FILE, 'a') as log_file:
                log_message = f"Chunk name: {filename}, Timestamp: {datetime.now()}, Target IP address: {client_address[0]}\n"
                log_file.write(log_message)
        finally:
            connection.close()

if __name__ == "__main__":
    start_server()
