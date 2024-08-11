from telekinesis.mobile_adapter.adapter import adapter
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
        "clientId": "9dae853f1ce82e85ed2537a301f4e33db77564f8",
        "timestamp": 0.009999999776482582,
        "goals": {
            "left": {
                "position_state": {
                    "x": -0.21616414189338684,
                    "y": 0.28979429602622986,
                    "z": 0.6324193477630615
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
                    "x": -0.13442760705947876,
                    "y": -0.10744979977607727,
                    "z": 0.7600054740905762
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