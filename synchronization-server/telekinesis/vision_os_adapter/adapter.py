from typing import TypedDict
from telekinesis.types import TelekinesisGoalType, JointLocalizerType, GraspMode

class JointPositions(TypedDict, total=False):
    ringFingerMetacarpal: JointLocalizerType
    thumbIntermediateBase: JointLocalizerType
    middleFingerIntermediateBase: JointLocalizerType
    ringFingerTip: JointLocalizerType
    ringFingerIntermediateTip: JointLocalizerType
    thumbTip: JointLocalizerType
    middleFingerTip: JointLocalizerType
    forearmWrist: JointLocalizerType
    ringFingerIntermediateBase: JointLocalizerType
    thumbKnuckle: JointLocalizerType
    littleFingerKnuckle: JointLocalizerType
    middleFingerMetacarpal: JointLocalizerType
    littleFingerTip: JointLocalizerType
    ringFingerKnuckle: JointLocalizerType
    indexFingerKnuckle: JointLocalizerType
    indexFingerTip: JointLocalizerType
    middleFingerIntermediateTip: JointLocalizerType
    thumbIntermediateTip: JointLocalizerType
    littleFingerIntermediateBase: JointLocalizerType
    middleFingerKnuckle: JointLocalizerType
    indexFingerMetacarpal: JointLocalizerType
    littleFingerMetacarpal: JointLocalizerType
    wrist: JointLocalizerType
    indexFingerIntermediateBase: JointLocalizerType
    littleFingerIntermediateTip: JointLocalizerType
    forearmArm: JointLocalizerType
    indexFingerIntermediateTip: JointLocalizerType

class HandData(TypedDict, total=False):
    isPinchGesture: bool
    jointPositions: JointPositions

class HandTrackingData(TypedDict):
    rightHand: HandData
    leftHand: HandData
    timestamp: int
    clientId: str    

def adapter(content: HandTrackingData) -> TelekinesisGoalType:
    base_template = {
        "clientId": content["clientId"],
        "timestamp": content["timestamp"],
        "goals": dict()
    }

    try: 
        rightWristContent = content["rightHand"]["jointPositions"]["wrist"]
    except KeyError:
        rightWristContent = None
    

    if rightWristContent is not None:
        base_template["goals"]["right"] = {
            "grasp_mode": GraspMode.CLOSE.value if bool(content.get("rightHand").get("isPinchGesture")) else GraspMode.OPEN.value,
            "position_state": rightWristContent["position"],
            "orientation_state": rightWristContent.get("orientation")
        }

    try:
        leftWristContent = content["leftHand"]["jointPositions"]["wrist"]
    except KeyError:
        leftWristContent = None

    if leftWristContent is not None:
        base_template["goals"]["left"] = {
            "grasp_mode": GraspMode.CLOSE.value if bool(content.get("leftHand").get("isPinchGesture")) else GraspMode.OPEN.value,
            "position_state": leftWristContent["position"],
            # TODO: Add rotation state
            "orientation_state": leftWristContent["orientation"]
        }

    return base_template