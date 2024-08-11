#!/usr/bin/env python

""" 
Simple script for testing server subscription.
"""
import asyncio
import websockets
import json

URI = "wss://droid-osmosis-1.onrender.com"

async def subscribe():
    while True: 
        async with websockets.connect(URI) as websocket:
            raw_byte_content = await websocket.recv()
            content = json.loads(raw_byte_content)
            print(content)


if __name__ == "__main__":
    asyncio.run(subscribe())