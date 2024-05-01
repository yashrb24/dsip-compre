import asyncio
import websockets

async def send_messages():
    async with websockets.connect("ws://localhost:8500") as websocket:
        while True:
            n = input("Enter an integer (or 'exit' to quit): ")
            if n.lower() == "exit":
                break
            await websocket.send(n)
            response = await websocket.recv()
            print("Server response:", response)

asyncio.run(send_messages())
