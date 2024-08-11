from typing import TypedDict, Dict
from telekinesis.types import TelekinesisGoalType, GraspMode, PositionType


class Finger(TypedDict):
    tip: PositionType
    distal: PositionType
    proximal: PositionType
    meta: PositionType

class HandData(TypedDict):
    wrist: PositionType
    palm: PositionType
    thumb: Finger
    index: Finger
    middle: Finger
    ring: Finger
    pinky: Finger

class HandTrackingData(TypedDict):
    clientId: str
    timestamp: float
    LeftHand: HandData
    RightHand: HandData

def adapter(content: HandTrackingData) -> TelekinesisGoalType:
    return {
        "clientId": content["clientId"],
        "timestamp": content["timestamp"],
        "goals": {
            "left": {
                "position_state": {
                    "x": content["LeftHand"]["wrist"]["x"],
                    "y": content["LeftHand"]["wrist"]["y"],
                    "z": content["LeftHand"]["wrist"]["z"]
                },
                # TODO: placeholder values, have to calc myself
                "orientation_state": {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 1
                },
                # TODO: placeholder have to calculate myself
                "grasp_mode": GraspMode.OPEN.value
            },
            "right": {
                "position_state": {
                    "x": content["RightHand"]["wrist"]["x"],
                    "y": content["RightHand"]["wrist"]["y"],
                    "z": content["RightHand"]["wrist"]["z"]
                },
                # TODO: placeholder values, have to calc myself
                "orientation_state": {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 1
                },
                # TODO: placeholder have to calculate myself
                "grasp_mode": GraspMode.OPEN.value
            }
        }
    }