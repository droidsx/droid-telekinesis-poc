extends MeshInstance3D

@export var goal_publisher: Node
@export var translationGain: int = 5

var position_offset: Vector3

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	goal_publisher.connect("end_effector_goal", _transform)


func _transform(data):
	var pos_state = data["position_state"] 	# [ x: meters, y, z]
	var orient_to = data["orientation_state"]   # Quaternion
	var grasp_mode = data["grasp_mode"] 		# opening | closing | holding
	var translate_to = Vector3(
		pos_state.x * translationGain,
		pos_state.y * translationGain,
		pos_state.z * translationGain)

	if not position_offset:
		position_offset = translate_to
	# Set position to given values -- the values received should be relative to the starting position - deltas
	position = translate_to - position_offset
	print("positions of handbox: ", position)

	var target = Quaternion(orient_to.x, orient_to.y, orient_to.z, orient_to.w)
	transform.basis = Basis(target)
	print("orientation: ", transform.basis)

	# Handle grasp mode (you can add your own logic here)
	if grasp_mode == "opening":
		print("Grasp mode: opening")
		# Add logic for opening the grasp
	elif grasp_mode == "closing":
		print("Grasp mode: closing")
		# Add logic for closing the grasp
	else:
		print(grasp_mode)
#
func _process(delta: float) -> void:
	pass
