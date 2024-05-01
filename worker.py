import sys
import asyncio
import websockets

async def handle_connection(websocket, path):
    try:
        async for message in websocket:
            try:
                n = int(message)
                if n < 1:
                    await websocket.send("Invalid input: Please provide a positive integer.")
                else:
                    result = sum(range(1, n + 1))
                    print(result)
            except ValueError:
                await websocket.send("Invalid input: Please provide an integer.")
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected.")

async def main():
    if len(sys.argv) < 2:
        print("Please provide a port number as a command line argument.")
        return

    port = int(sys.argv[1])
    async with websockets.serve(handle_connection, "localhost", port):
        print(f"Server started. Listening for connections on port {port}...")
        await asyncio.Future()  # Keep the server running indefinitely

asyncio.run(main())

