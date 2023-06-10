import os
import socket
import json
import time

CHUNK_SIZE = 0
BROADCAST_IP = '255.255.255.255'
BROADCAST_PORT = 5001

def divide_file(file_path):
    filename, extension = os.path.splitext(file_path)
    with open(file_path, 'rb') as file_handle:
        data = file_handle.read()
        total_size = len(data)
        chunk_size = total_size // 4
        chunks = [data[i:i + chunk_size] for i in range(0, total_size, chunk_size)]
        for i, chunk in enumerate(chunks):
            chunk_filename = f'{filename}_{i+1}'
            with open(chunk_filename, 'wb') as chunk_file_handle:
                chunk_file_handle.write(chunk)
        return len(chunks)

def list_files(directory):
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def broadcast_files(directory):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        file_list = list_files(directory)
        message = json.dumps({'chunks': file_list}).encode('utf-8')
        sock.sendto(message, (BROADCAST_IP, BROADCAST_PORT))
        time.sleep(2)  # Broadcast every 2 seconds

def main():
    file_path = input('Please enter the directory of the file you want to share: ')
    print(file_path)
    directory = os.path.dirname(file_path)
    if directory == '':
        directory = '.'
    chunk_count = divide_file(file_path)
    print(f'{chunk_count} chunks have been created. Starting the announcement process...')
    broadcast_files(directory)

if __name__ == "__main__":
    main()
