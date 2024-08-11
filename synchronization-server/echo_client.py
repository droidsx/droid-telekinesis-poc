#!/usr/bin/env python

""" 
Simple script for testing server is up. The server should send back whatever you give it.
"""
import asyncio
import websockets
import os

URI = os.environ['URI'] or 'wss://droid-osmosis-1.onrender.com'

async def hello():
    while True: 
        async with websockets.connect(URI) as websocket:
            # If you comment these input lines then this script will simply receive broadcasted messages. To test you can run this script as is (as a publisher) and then run another instance of this script without the input lines (as a subscriber).
            something = input("Say something for the server to echo back: ")
            await websocket.send(something)
            print(f">>> {something}")

            echo = await websocket.recv()
            print(f"<<< {echo}")

if __name__ == "__main__":
    asyncio.run(hello())