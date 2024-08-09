extends MeshInstance3D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var publisher = get_node("../WebSocketClient")
	publisher.connect("end_effector_goal_changes", _transform)


func _transform(data):
	print(data)
	var translate_to = data["position_state"] 	# [ x: meters, y, z]
	var rotate_to = data["rotation_state"] 		# [ x: radians, y, z ]
	var grasp_mode = data["grasp_mode"] 		# opening | closing

	# Set position to given values -- the values received should be relative to the starting position - deltas
	translate(Vector3(translate_to[0], translate_to[1], translate_to[2]))

	# TODO:
	## Set the rotation of the block (assuming rotation is in radians)
	#var new_rotation = Vector3(rotate_to[0], rotate_to[1], rotate_to[2])
	#rotation = new_rotation
#
	# TODO:
	## Handle grasp mode (you can add your own logic here)
	#if grasp_mode == "opening":
		#print("Grasp mode: opening")
		## Add logic for opening the grasp
	#elif grasp_mode == "closing":
		#print("Grasp mode: closing")
		## Add logic for closing the grasp
#
	#print("Position set to: ", new_position)
	#print("Rotation set to: ", new_rotation)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
