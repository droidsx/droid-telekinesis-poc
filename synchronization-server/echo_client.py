#!/usr/bin/env python

""" 
Simple script for testing server is up and echoing back.
"""
import asyncio
import websockets

URI = "wss://droid-osmosis.onrender.com"

async def hello():
    while True: 
        async with websockets.connect(URI) as websocket:
            # If you comment these input lines then this script will simply receive broadcasted messages. To test you can run this script as is (as a publisher) and then run another instance of this script without the input lines (as a subscriber).
            name = input("What's your name? ")
            await websocket.send(name)
            print(f">>> {name}")

            greeting = await websocket.recv()
            print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())