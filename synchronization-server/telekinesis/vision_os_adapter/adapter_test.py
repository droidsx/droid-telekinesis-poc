import json
import os

import pytest

from telekinesis.vision_os_adapter.adapter import adapter

@pytest.fixture
def success_fixture():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return json.loads(open(os.path.join(dir_path, "success_fixture.json"), encoding="utf-8").read())


# Use the wrist as the goal position
def test_transform(success_fixture):
    goals = adapter(success_fixture)
    assert goals == {
        "timestamp": 1724102548,
        "clientId": "DFEF841C-9442-4936-8F11-9C3595546A35",
        "goals": {
            "left": {
                "position_state": {
                    "y": 0.8093888759613037,
                    "x": -0.24577036499977112,
                    "z": -0.27957069873809814
                },
                "orientation_state": {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 1
                },
                "grasp_mode": "OPEN"
            },
            "right": {
                "position_state": {
                    "y": 0.8037000298500061,
                    "x": -0.009675380773842335,
                    "z": -0.3731447756290436
                },
                "orientation_state": {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 1
                },
                "grasp_mode": "OPEN"
            }
        }
    }

@pytest.mark.parametrize("missing_hand, missing_key", [("rightHand", "right"), ("leftHand", "left")])
def test_missing_hand(success_fixture, missing_hand, missing_key):
    success_fixture.pop(missing_hand)

    goals = adapter(success_fixture)

    assert goals.get("goals").get(missing_key) is None
    