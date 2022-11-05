import socket
import os
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def server_run():
    # Get Host info
    host = socket.gethostname()

    # Create and bind socket
    server_socket = socket.socket()
    server_socket.bind((host, PORT))

    server_socket.listen()
    conn, address = server_socket.accept()
    print(f"Connected to {address}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if str(data) == 'sendfile':
            receiveFile(conn)
        else:
            print(f"User: {str(data)}")
        
        message = sendInfo(conn)
        if message.lower().strip() == 'exit':
            break

    conn.close()

def receiveFile(conn):
    # Wait for file name
    filename = conn.recv(SIZE).decode(FORMAT)
    print(f"[File] Receiving the filename.")
    conn.send("Filename received.".encode(FORMAT))

    # Wait for file size.
    filesize = conn.recv(SIZE).decode(FORMAT)
    print(f"[File] Receiving the filesize.")
    conn.send("Filesize received.".encode(FORMAT))

    # Wait for file data
    data = conn.recv(int(filesize))
    print(f"[File] Receiving the file data.")

    # Write to File
    file = open(filename, "wb")
    file.write(data)
    conn.send("File received".encode(FORMAT))
    file.close()

def sendFile(conn, filepath):
    # Open and read file
    file = open(filepath, "rb")
    data = file.read()

    # Send File Name
    conn.send(os.path.basename(filepath).encode(FORMAT))
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"[User]: {msg}")

    # Send File Size
    conn.send(f"{len(data)}".encode(FORMAT))
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"[User]: {msg}")
    
    # Send the File Data
    conn.send(data)
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"[User]: {msg}")

    # Close File
    file.close()

def sendInfo(this_socket):
    message = input(" -> ")
    if message.strip() == 'sendfile':
        this_socket.send(message.encode())
        filepath = input("enter filepath: ")

        sendFile(this_socket, filepath)
    elif message.lower().strip() != 'exit':
        this_socket.send(message.encode())
    return message

if __name__ == '__main__':
    server_run()