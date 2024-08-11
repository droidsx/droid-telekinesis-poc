#!/usr/bin/env python

import asyncio
import websockets
import os
import json

connected = set()
PORT = os.environ.get('PORT', 8765)

"""
This is a middleware that takes incoming data from a client controller, pre-processes it to a standard tele-operation format, and broadcasts it to connected clients. 
"""
async def handler(websocket):
    print('received websocket connection: ', websocket)
    connected.add(websocket)
    
    async for message in websocket:
        try: 
            print('received message and broadcasting: ', message)
            # Transform message to Telekinesis format
            inbound = json.loads(message)

            isMobileClient = content.get('RightHand', None) is not None
            isVisionOSClient = content.get('leftHand', None) is not None
            outbound = inbound

            if isMobileClient:
                # Transform to Telekinesis format
                outbound = adapter(content)
            elif isVisionOSClient:
                # Transform to Telekinesis format
                outbound = adapter(content)

            websockets.broadcast(connected, json.dumps(outbound))
        except Exception as e:
            print(e)
            break

async def main():
    print('server started on 0.0.0.0:', PORT)
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())