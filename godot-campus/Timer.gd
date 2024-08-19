extends Timer

signal end_effector_goal(json_data)
# We can use this to test our setup without needing to use data from the websocket.
# Every second we will publish updated positional data through the signal
var out_and_back_on_each_axis = [
	{
		"position_state": {
			"x": 0,
			"y": 0,
			"z": 0
		},
	},
	{
		"position_state": {
			"x": 3,
			"y": 0,
			"z": 0
		},
	},
	{
		"position_state": {
			"x": 0,
			"y": 0,
			"z": 0
		},
	},
	{
		"position_state": {
			"x": 0,
			"y": 3,
			"z": 0
		},
	},
	{
		"position_state": {
			"x": 0,
			"y": 0,
			"z": 0
		},
	},
	{
		"position_state": {
			"x": 0,
			"y": 0,
			"z": 3
		},
	},
]
var current_goal_index = 0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _set_next_goal() -> void:
	if current_goal_index < len(out_and_back_on_each_axis):
		emit_signal("end_effector_goal", out_and_back_on_each_axis[current_goal_index])
		current_goal_index += 1


func _on_timeout() -> void:
	_set_next_goal() # Replace with function body.
