import asyncio


clients = []
nicknames = []

async def send_all_clients(message, sender=None, clients=clients):
    """sends a message to all clients"""
    for client in clients:
        if client != sender:
            msg = message.encode('utf-8') 
            client.write(msg)

async def handle(reader, writer):
    """handles a single client"""
    clients.append(writer)
    writer.write("Nickname".encode('utf-8'))
    nickname = (await reader.read(100)).decode('utf-8')
    await send_all_clients(f'{nickname} joined the chat!')
    print(f'{nickname} joined the chat!')
    nicknames.append(nickname)
    while True:
        try:
            data = await reader.read(100)
        except:
            print("Closed the connection with {}".format(nickname))
            break
        message = data.decode('utf-8')
        await send_all_clients(message, writer)

    writer.close()
    index = clients.index(writer)
    remove_nickname = nicknames[index]
    nicknames.remove(remove_nickname)
    clients.remove(writer)
    await send_all_clients(f'{remove_nickname} left the chat!')

async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 10000)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Running the server on: {addrs}')
    async with server:
        await server.serve_forever()


asyncio.run(main())