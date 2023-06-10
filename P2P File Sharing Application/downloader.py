import socket
import json
from datetime import datetime

TCP_PORT = 5000

def download_file_chunk(ip_address, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip_address, TCP_PORT))
        message = json.dumps({"requestedcontent": filename}).encode('utf-8')
        sock.sendall(message)
        chunk_data = sock.recv(1048576)
        return chunk_data
    finally:
        sock.close()

def merge_chunks(filename, start_chunk, end_chunk):
    with open(f"{filename}.png", 'wb') as output_file:
        for i in range(start_chunk, end_chunk):
            chunk_name = f"{filename}_{i+1}"
            with open(chunk_name, 'rb') as chunk_file:
                output_file.write(chunk_file.read())

def main():
    start_chunk = 0
    end_chunk = 5  # Excluding 5

    with open('content_dictionary.txt', 'rb') as file_handle:
        content_dictionary = json.load(file_handle)

    filename = input("Enter the name of the file you want to download: ")

    for i in range(start_chunk, end_chunk):
        chunk_name = f"{filename}_{i+1}"
        if chunk_name not in content_dictionary:
            print(f"CHUNK {chunk_name} CANNOT BE DOWNLOADED FROM ONLINE SOURCES.")
            continue

        for ip_address in content_dictionary[chunk_name]:
            try:
                chunk_data = download_file_chunk(ip_address, chunk_name)
                with open(chunk_name, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)
                print(f"{chunk_name} successfully downloaded from {ip_address}.")
                with open('download_log.txt', 'a') as log_file:
                    log_file.write(f"{datetime.now()}: {chunk_name} downloaded from {ip_address}\n")
                break
            except Exception as e:
                print(f"{chunk_name} couldn't be downloaded from {ip_address}: {e}")
        else:
            print(f"CHUNK {chunk_name} CANNOT BE DOWNLOADED FROM ONLINE SOURCES.")

    merge_chunks(filename, start_chunk, end_chunk)

    # Perform file upload to the server here

    print(f"{filename}.png chunks {start_chunk}-{end_chunk-1} successfully downloaded and merged.")

if __name__ == "__main__":
    main()