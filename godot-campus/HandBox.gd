extends MeshInstance3D

@export var goal_publisher: Node
@export var translationGain: int = 5

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	goal_publisher.connect("end_effector_goal", _transform)


func _transform(data):
	var translate_to = data["position_state"] 	# [ x: meters, y, z]
	var orient_to = data["orientation_state"] # Quaternion
	# var grasp_mode = data["grasp_mode"] 		# opening | closing

	# Set position to given values -- the values received should be relative to the starting position - deltas
	position = Vector3(
		translate_to.x * translationGain,
		translate_to.y * translationGain,
		translate_to.z * translationGain)
	print("positions of handbox: ", position)

	var target = Quaternion(orient_to.x, orient_to.y, orient_to.z, orient_to.w)
	transform.basis = Basis(target)
	print("orientation: ", transform.basis)

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

func _process(delta: float) -> void:
	pass
