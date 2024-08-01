extends RigidBody3D


const TARGET_SPEED = 5.0
var _pid := PID3D.new(1.0, 0.1, 1.0)


func _physics_process(delta: float) -> void:
	var direction = Vector3(
		Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left"),
		0.0,
		Input.get_action_strength("ui_up") - Input.get_action_strength("ui_down")
	).normalized()
	var target_velocity = direction * TARGET_SPEED
	var velocity_error = target_velocity - linear_velocity
	var correction_impulse = _pid.update(velocity_error, delta) * 0.01
	apply_central_impulse(correction_impulse)
