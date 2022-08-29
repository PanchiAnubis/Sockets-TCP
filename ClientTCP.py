import socket
import threading

host = '127.0.0.1' #local host
port = 55555 #puerto libre

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def recieve_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error ocurred")
            client.close()
            break
    
def write_messages():
    while True:
        message = f"{username} : {input('')}"
        client.send(message.encode("utf-8"))

recieve_thread = threading.Thread(target=recieve_messages)
recieve_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()