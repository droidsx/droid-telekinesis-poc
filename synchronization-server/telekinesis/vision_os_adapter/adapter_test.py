from telekinesis.vision_os_adapter.adapter import adapter
import json
import pytest
import os


@pytest.fixture
def success_fixture():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return json.loads(open(os.path.join(dir_path, "success_fixture.json")).read())


# Use the wrist as the goal position
def test_transform(success_fixture):
    goals = adapter(success_fixture)
    assert goals == {
        "clientId": "DFEF841C-9442-4936-8F11-9C3595546A35",
        "timestamp": 1723077231,
        "goals": {
            "left": {
                "position_state": {
                    "y": 0.3483285903930664,
                    "x": 3.0620064735412598,
                    "z": -10.524316787719727
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
                    "y": 0.312869668006897,
                    "x": 2.875335931777954,
                    "z": -10.420853614807129
                },
                "orientation_state": {
                    "x": 0,
                    "y": 0,
                    "z": 0,
                    "w": 1
                },
                "grasp_mode": "CLOSE"
            }
        }
    }