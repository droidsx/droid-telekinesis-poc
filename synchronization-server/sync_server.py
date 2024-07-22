#!/usr/bin/env python

import asyncio
import websockets
import os

connected = set()
PORT = os.environ.get('PORT', 8765)

"""
This is a middleware that takes incoming data from a client and broadcasts it to all clients.
"""
async def handler(websocket):
    print('received websocket connection: ', websocket)
    connected.add(websocket)
    
    async for message in websocket:
        try: 
            print('received message and broadcasting: ', message)
            websockets.broadcast(connected, message)
        except Exception as e:
            print(e)
            break

async def main():
    print('server started on 0.0.0.0:', PORT)
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())