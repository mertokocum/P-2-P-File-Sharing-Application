import os
import socket
import json

LISTEN_IP = '0.0.0.0'
BROADCAST_PORT = 5001
BUFFER_SIZE = 1048576

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, BROADCAST_PORT))

content_dictionary = {}


def main():
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = json.loads(data.decode('utf-8'))

        files = message.get('chunks', [])

        for file in files:
            # Check if the file name contains an underscore and the part after the underscore doesn't contain a period
            if '_' in file and '.' and 'txt' not in file and file.split('_')[1:]:
                # Add only files with the target extension
                if file not in content_dictionary:
                    content_dictionary[file] = [addr[0]]
                    print(f"New file detected: {addr[0]} : {file}")
                elif addr[0] not in content_dictionary[file]:
                    content_dictionary[file].append(addr[0])
                    print(f"For {file}, new IP address detected: {addr[0]}")

        with open('content_dictionary.txt', 'w') as file_handle:
            file_handle.write(json.dumps(content_dictionary, indent=4))


if __name__ == "__main__":
    main()
