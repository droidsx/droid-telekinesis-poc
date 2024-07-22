#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "ws://droid-osmosis.onrender.com:8765"
    while True: 
        async with websockets.connect(uri) as websocket:
            # If you comment these input lines then this script will simply receive broadcasted messages. To test you can run this script as is (as a publisher) and then run another instance of this script without the input lines (as a subscriber).
            name = input("What's your name? ")
            await websocket.send(name)
            print(f">>> {name}")

            greeting = await websocket.recv()
            print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())