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
                    await websocket.send(f"The sum of integers from 1 to {n} is {result}.")
            except ValueError:
                await websocket.send("Invalid input: Please provide an integer.")
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected.")

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Server started. Listening for connections...")
        await asyncio.Future()  # Keep the server running indefinitely

asyncio.run(main())
