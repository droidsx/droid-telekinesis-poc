#!/usr/bin/env python

import asyncio
import websockets
import os
import json
from json import JSONDecodeError
from telekinesis.mobile_adapter.adapter import adapter

connections = set()
PORT = os.environ.get('PORT', 8765)

"""
This is a middleware that takes incoming data from a client controller, pre-processes it to a standard tele-operation format, and broadcasts it to connected clients. 
"""
async def handler(websocket):
    connections.add(websocket)

    print('received websocket connection: ', websocket)    
    async for message in websocket:
        # Transform message to Telekinesis format
        try: 
            content = json.loads(message)
            print('received message: ', content)

            isMobileClient = content.get('RightHand', None) is not None
            isVisionOSClient = content.get('leftHand', None) is not None

            if isMobileClient:
                # Transform to Telekinesis format
                content = adapter(content)
            elif isVisionOSClient:
                # Transform to Telekinesis format
                content = adapter(content)
            print('broadcasting: ', content)
            websockets.broadcast(connections, json.dumps(content))

        except JSONDecodeError as e:
            print('Error decoding JSON: ', e)
            print('Message received was not JSON: ', message)
            print('Broadcasting: ', message)
            websockets.broadcast(connections, message)
        
        finally:
            print('Error occurred while processing message: ', message)

async def main():
    print('server started on 0.0.0.0:', PORT)
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())