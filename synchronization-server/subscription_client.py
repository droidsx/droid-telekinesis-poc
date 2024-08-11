#!/usr/bin/env python

""" 
Simple script for testing server is up and echoing back.
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

            # For now we don't have a nice way to determine client type
            # so just try it and if it fails go on to the next one
            try: 
                print("trying vision OS adapter...")
                print(droid_telekinesis_visionOS_adapter(content))
                print("vision OS adapter successful")
            except KeyError as e:
                print("Failed to adapt for client: VisionOS")
                print(e)

                try: 
                    print("trying iOS adapter...")
                    print(droid_telekinesis_ios_adapter(content))
                    print("ios adapter successful")
                except KeyError as e:
                    print("Failed to adapt for client: iOS")
                    print(e)


if __name__ == "__main__":
    asyncio.run(subscribe())