from Objects_smooth import Net, Apple, Snake, Screen

import socket
import pickle


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((Net.host, Net.port))

    clients = []

    print('Start Server')
    apple = Apple()
    snake = Snake()
    apple.spawn(snake, Screen.height, Screen.width, False)
    dict_of_data = {}
    while True:

        data, address = server.recvfrom(1024)

        pickled_data = pickle.loads(data)
        apple_body = (apple.x, apple.y)
        snake_body = pickled_data["Snake"]
        is_eaten = pickled_data["Is eaten"]
        score = pickled_data["Score"]

        if is_eaten:
            apple.spawn(snake, Screen.height, Screen.width, False)
            apple_body = (apple.x, apple.y)
        if address not in clients:
            clients.append(address)

        dict_of_data["Score"] = score
        dict_of_data["Apple"] = apple_body
        dict_of_data["Snake"] = snake_body

        data = pickle.dumps(dict_of_data)

        for client in clients:
            if client == address:
                continue
            server.sendto(data, client)

        dict_of_data.clear()
