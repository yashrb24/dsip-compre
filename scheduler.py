import asyncio
import websockets
from flask import Flask, request


app = Flask(__name__)
ports = [8500, 8501, 8502, 8503, 8504, 8505]
current_port_idx = 0

async def send_messages(number):
    global current_port_idx
    async with websockets.connect(f"ws://localhost:{ports[current_port_idx]}") as websocket:
        await websocket.send(str(number))
        current_port_idx  = (1 + current_port_idx) % len(ports)

@app.route('/sum', methods=['POST'])
def sum():
    global current_port_idx
    number = int(request.form['number'])
    asyncio.run(send_messages(number))  # Run the coroutine in the event loop
    return f"Task scheduled at worker{current_port_idx}. Go back to the homepage to schedule another task."

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # Run the Flask app
