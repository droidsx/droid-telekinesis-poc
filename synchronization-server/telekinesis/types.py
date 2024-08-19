from typing import TypedDict, Dict
from enum import Enum


class PositionType(TypedDict, total=False):
    x: float
    y: float
    z: float


class QuaternionType(TypedDict, total=False):
    x: float
    y: float
    z: float
    w: float


class JointLocalizerType(TypedDict, total=False):
    position: PositionType
    orientation: QuaternionType


class GraspMode(Enum):
    OPEN = "OPEN"
    HOLD = "HOLD"
    CLOSE = "CLOSE"


class ManipulatorType(TypedDict, total=False):
    position_state: PositionType
    orientation_state: QuaternionType
    grasp_mode: GraspMode


class BimanualManipulatorType(TypedDict, total=False):
    left: ManipulatorType
    right: ManipulatorType


# TODO: we will want to flush this spec out -- what things can a human show the robot? 
# I want to record pressure so that I can eliminate grasp mode all together 
class TelekinesisGoalType(TypedDict, total=False):
    goals: BimanualManipulatorType
    timestamp: int
    clientId: str


