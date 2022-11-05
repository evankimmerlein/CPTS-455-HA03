import socket
import os
IP = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def client_run():
    host = socket.gethostname()

    client_socket = socket.socket()
    client_socket.connect((host,PORT))

    print("Type 'sendfile' to send a file, 'exit' to exit, or anything else to send a message")
    message = "start loop"

    while message.lower().strip() != 'exit':

        message = sendInfo(client_socket)

        if message.lower().strip() == 'exit':
            break

        data = client_socket.recv(1024).decode()
        if not data:
            break

        if str(data) == 'sendfile':
            receiveFile(client_socket)
        else:
            print(f"Server: {str(data)}")


    client_socket.close()

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
    conn.send("File data received".encode(FORMAT))
    file.close()

def sendFile(conn, filepath):
    # Open and read file
    file = open(filepath, "rb")
    data = file.read()
    # Send File Name
    conn.send(os.path.basename(filepath).encode(FORMAT))
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"[Server]: {msg}")
    # Send File Size
    conn.send(f"{len(data)}".encode(FORMAT))
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"[Server]: {msg}")
    #Send the File Data
    conn.send(data)
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"[Server]: {msg}")

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
    client_run()