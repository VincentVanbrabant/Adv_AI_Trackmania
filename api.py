import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9000))
print('Connected')

while True:
    try:
        response = client.recv(1024)
        cp, time = int.from_bytes(response[:1], byteorder='little', signed=True),\
            int.from_bytes(response[1:], byteorder='little', signed=False)
        print(f'checkpoint: {cp}')
        print(f'time: {time}')
    except KeyboardInterrupt as e:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        break
