import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))


    if 'palm.cpu' in message:
        message = "ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n"
        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

    print("Close the client socket")
    writer.close()
# mikecheck
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8887, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()