from Objects_smooth import Net, Apple, Snake, Screen

import socket
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((Net.host, Net.port))

clients = []

print('Start Server')
apple = Apple()
snake = Snake()
apple.spawn(snake, Screen.height, Screen.width, False)
list_of_data = []
while True:

    data, address = server.recvfrom(1024)

    apple_body = (apple.x, apple.y)
    snake_body = pickle.loads(data)[0]
    is_eaten = pickle.loads(data)[1]

    if is_eaten:
        apple.spawn(snake, Screen.height, Screen.width, False)
        apple_body = (apple.x, apple.y)
    if address not in clients:
        clients.append(address)

    list_of_data.append(apple_body)
    list_of_data.append(snake_body)

    data = pickle.dumps(list_of_data)

    for client in clients:
        if client == address:
            continue
        server.sendto(data, client)

    list_of_data.clear()
