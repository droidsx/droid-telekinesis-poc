#!/usr/bin/env python

import asyncio
import websockets

connected = set()

"""
This is a middleware that takes incoming data from a client and broadcasts it to all clients.
"""
async def handler(websocket):
    print('received websocket connection: ', websocket)
    connected.add(websocket)
    
    async for message in websocket:
        try: 
            websockets.broadcast(connected, message)
        except Exception as e:
            print(e)
            break

async def main():
    print('server started on localhost:8765')
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())