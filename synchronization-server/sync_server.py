#!/usr/bin/env python
import asyncio

import websockets
import os
import json
from telekinesis.mobile_adapter.adapter import adapter as mobile_adapter
from telekinesis.vision_os_adapter.adapter import adapter as vision_os_adapter
from telekinesis.types import TelekinesisGoalType

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
        content = transform_message_to_telekinesis_format(content)
        print('broadcasting: ', content)
        websockets.broadcast(connections, json.dumps(content))


def transform_message_to_telekinesis_format(content) -> TelekinesisGoalType:
    client_type = content.get('client_type')
        
    if client_type == 'ios':
        # Transform to Telekinesis format
        content = mobile_adapter(content)
    # FIXME: Use quick hack -- only vision os controller has rightHand field
    # this is a temporary solution until we have a better way to identify the client type
    # like explicitly passing it
    elif client_type == 'vision_os' or content.get('rightHand'):
        # Transform to Telekinesis format
        content = vision_os_adapter(content)
    else:
        print('Client type not recognized')
        print('vision_os: ', content.get('rightHand'))
        return None

    return content

        
async def main():
    print('server started on 0.0.0.0:', PORT)
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())