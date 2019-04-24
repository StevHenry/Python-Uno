import asyncio


@asyncio.coroutine
def tcp_echo_client(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8800, loop=loop)

    print('Sending: %r' % message)
    writer.write(message.encode())

    data = yield from reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()


message = 'Hello World!'
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(tcp_echo_client(message, loop))
    loop.close()
except ConnectionRefusedError:
    print("Connexion impossible")
