import socket
import threading

host = '127.0.0.1' #local host
port = 55555 #puerto libre

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #almacenar el socket en una variable que en este caso es el server

server.bind((host, port)) #para pasar los datos de conexion que el servidor va a tener

server.listen() #que este a la escucha de conexiones de los clientes

print(f"Server running on {host} : {port}")


clients = [] #almacenar las conexiones de los clientes
usernames = [] #los usernames de cada cliente

def broadcast(message, clientSend): #enviar el mensaje a todos los clientes
    #clientSend, cliente que envio el mensaje
    for client in clients:
        if client != clientSend:
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024) #1024 bytes, limite de lectura
            broadcast(message, client)
        except: #Por si ocurre un error
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"Aviso: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def recieve_connections():

    while True:
        #aceptar las conexiones de los clientes
        client, address = server.accept()

        client.send("@username".encode("utf-8")) #el servidos solicita el username al cliente
        username = client.recv(1024).decode("utf-8")

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"Aviso: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        #hilo
        thread.start()

recieve_connections()