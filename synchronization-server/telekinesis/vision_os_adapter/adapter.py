from typing import TypedDict, Dict
from telekinesis.types import TelekinesisGoalType, PositionType, GraspMode

class JointPositions(TypedDict, total=False):
    ringFingerMetacarpal: PositionType
    thumbIntermediateBase: PositionType
    middleFingerIntermediateBase: PositionType
    ringFingerTip: PositionType
    ringFingerIntermediateTip: PositionType
    thumbTip: PositionType
    middleFingerTip: PositionType
    forearmWrist: PositionType
    ringFingerIntermediateBase: PositionType
    thumbKnuckle: PositionType
    littleFingerKnuckle: PositionType
    middleFingerMetacarpal: PositionType
    littleFingerTip: PositionType
    ringFingerKnuckle: PositionType
    indexFingerKnuckle: PositionType
    indexFingerTip: PositionType
    middleFingerIntermediateTip: PositionType
    thumbIntermediateTip: PositionType
    littleFingerIntermediateBase: PositionType
    middleFingerKnuckle: PositionType
    indexFingerMetacarpal: PositionType
    littleFingerMetacarpal: PositionType
    wrist: PositionType
    indexFingerIntermediateBase: PositionType
    littleFingerIntermediateTip: PositionType
    forearmArm: PositionType
    indexFingerIntermediateTip: PositionType

class HandData(TypedDict, total=False):
    isPinchGesture: bool
    jointPositions: JointPositions

class HandTrackingData(TypedDict):
    rightHand: HandData
    leftHand: HandData
    timestamp: int
    clientId: str    

def adapter(content: HandTrackingData) -> TelekinesisGoalType:
    try: 
        rightWristContent = content["rightHand"]["jointPositions"]["wrist"]
    except KeyError:
        rightWristContent = None
    
    try:
        leftWristContent = content["leftHand"]["jointPositions"]["wrist"]
    except KeyError:
        leftWristContent = None


    base_template = {
        "clientId": content["clientId"],
        "timestamp": content["timestamp"],
        "goals": dict()
    }

    if rightWristContent is not None:
        base_template["goals"]["right"] = {
            "grasp_mode": GraspMode.CLOSE.value if bool(content.get("rightHand").get("isPinchGesture")) else GraspMode.OPEN.value,
            "position_state": {
                "z": rightWristContent["position"]["z"],
                "y": rightWristContent["position"]["y"],
                "x": rightWristContent["position"]["x"]
            },
            # TODO: Add rotation state, have to calculate myself
            "orientation_state": {
                "x": 0,
                "y": 0,
                "z": 0,
                "w": 1
            },
        }

    if leftWristContent is not None:
        base_template["goals"]["left"] = {
            "grasp_mode": GraspMode.CLOSE.value if bool(content.get("leftHand").get("isPinchGesture")) else GraspMode.OPEN.value,
            "position_state": {
                "z": leftWristContent["position"]["z"],
                "y": leftWristContent["position"]["y"],
                "x": leftWristContent["position"]["x"]
            },
            # TODO: Add rotation state
            "orientation_state": {
                "x": 0,
                "y": 0,
                "z": 0,
                "w": 1
            },
        }

    return base_template