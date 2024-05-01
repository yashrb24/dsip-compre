import asyncio
import websockets
from flask import Flask, request

app = Flask(__name__)
ports = [8500, 8501, 8502, 8503, 8504, 8505]
current_port_idx = 0
task_queue = asyncio.Queue()  # Queue to store pending tasks
lock = asyncio.Lock()  # Lock to synchronize access to the queue


async def send_messages(number, port):
    async with websockets.connect(f"ws://localhost:{port}") as websocket:
        await websocket.send(str(number))
        response = await websocket.recv()
        print(f"Received response from worker at port {port}: {response}")


async def worker(port):
    while True:
        async with lock:
            if not task_queue.empty():
                number, port = await task_queue.get()  # Wait for a task from the queue
                await send_messages(number, port)
                task_queue.task_done()  # Mark the task as done
            else:
                await asyncio.sleep(0.1)  # Sleep briefly if the queue is empty


async def main():
    # Start worker tasks
    worker_tasks = [asyncio.create_task(worker(port)) for port in ports]

    # Run the Flask app
    app.run(port=5001, debug=True)

    # Wait for worker tasks to complete
    await asyncio.gather(*worker_tasks)


@app.route('/sum', methods=['POST'])
def sum():
    global current_port_idx
    number = int(request.form['number'])
    port = ports[current_port_idx]
    current_port_idx = (current_port_idx + 1) % len(ports)
    task_queue.put_nowait((number, port))  # Put the task in the queue
    return f"Task scheduled at worker {port}. Go back to the homepage to schedule another task."


if __name__ == '__main__':
    asyncio.run(main())
