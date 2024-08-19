#!/usr/bin/env python

import asyncio
import websockets
import os
import json
from json import JSONDecodeError
from telekinesis.mobile_adapter.adapter import adapter as mobile_adapter
from telekinesis.vision_os_adapter.adapter import adapter as vision_os_adapter

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
        print('Message received: ', message)
        content = json.loads(message)

        client_type = content.get('client_type')
        print("client type is: ", client_type)
            
        if client_type == 'ios':
            # Transform to Telekinesis format
            content = mobile_adapter(content)
        elif client_type == 'vision_os':
            # Transform to Telekinesis format
            content = vision_os_adapter(content)
        else:
            raise Exception('Unknown client type')
            
        print('broadcasting: ', content)
        websockets.broadcast(connections, json.dumps(content))
        

        
async def main():
    print('server started on 0.0.0.0:', PORT)
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())