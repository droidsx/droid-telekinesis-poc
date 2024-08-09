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
            # print(f"<<< {content}")

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
            
# Our goal with the below adapters is to simply provide end effector goal positions for the end client, discrete action values like for opening and closing the gripper, and rotation values of the end effector.

""" 
Example of content, these are the joint pos in vision OS all with XYZ for the right and left hands.
{
  "rightHand": {
    "isPinchGesture": false,
    "jointPositions": {
      "ringFingerMetacarpal": {
        "z": -1.7121222019195557,
        "y": 0.7230986952781677,
        "x": -8.659623146057129
      },
      "thumbIntermediateBase": {
      },
      "middleFingerIntermediateBase": {
      },
      "ringFingerTip": {
      },
      "ringFingerIntermediateTip": {
      },
      "thumbTip": {
      },
      "middleFingerTip": {
      },
      "forearmWrist": {
      },
      "ringFingerIntermediateBase": {
      },
      "thumbKnuckle": {
      },
      "littleFingerKnuckle": {
      },
      "middleFingerMetacarpal": {
      },
      "littleFingerTip": {
      },
      "ringFingerKnuckle": {
      },
      "indexFingerKnuckle": {
      },
      "indexFingerTip": {
      },
      "middleFingerIntermediateTip": {
      },
      "thumbIntermediateTip": {
      },
      "littleFingerIntermediateBase": {
      },
      "middleFingerKnuckle": {
      },
      "indexFingerMetacarpal": {
      },
      "littleFingerMetacarpal": {
      },
      "wrist": {
      },
      "indexFingerIntermediateBase": {
      },
      "littleFingerIntermediateTip": {
      },
      "forearmArm": {
      },
      "indexFingerIntermediateTip": {
      }
    }
  },
  "timestamp": 1723075278,
  "clientId": "DFEF841C-9442-4936-8F11-9C3595546A35",
  "leftHand": {
    ... same as right hand
  }
}
"""
def droid_telekinesis_visionOS_adapter(content):
    return {
        "position_state": {
                "z": content["rightHand"]["jointPositions"]["wrist"]["z"],
                "y": content["rightHand"]["jointPositions"]["wrist"]["y"],
                "x": content["rightHand"]["jointPositions"]["wrist"]["x"]
            }
    }
    return {
        "rightHand": {
            "grasp_mode": bool(content["rightHand"]["isPinchGesture"]),
            "position_state": {
                "z": content["rightHand"]["jointPositions"]["wrist"]["z"],
                "y": content["rightHand"]["jointPositions"]["wrist"]["y"],
                "x": content["rightHand"]["jointPositions"]["wrist"]["x"]
            },
            # TODO: Add rotation state
            "rotation_state": {
                "z": 0,
                "y": 0,
                "x": 0
            }
        },
        "leftHand": {
            "grasp_mode": bool(content["leftHand"]["isPinchGesture"]),
            "position_state": {
                "z": content["leftHand"]["jointPositions"]["wrist"]["z"],
                "y": content["leftHand"]["jointPositions"]["wrist"]["y"],
                "x": content["leftHand"]["jointPositions"]["wrist"]["x"]
            },
            # TODO: Add rotation state
            "rotation_state": {
                "z": 0,
                "y": 0,
                "x": 0
            }
        },
    }


def droid_telekinesis_ios_adapter(content):
    pass


if __name__ == "__main__":
    asyncio.run(subscribe())