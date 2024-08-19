#extends Camera3D
#
#var rotation_speed = 0.005
#var move_speed = 10.0
#
#func _ready():
	## Lock the mouse to the center of the screen
	#Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
#
#func _process(delta):
	## Rotate the camera based on mouse movement
	#var mouse_delta = get_viewport().get_mouse_position()
	#rotate_y(-mouse_delta.x * rotation_speed)
	#rotate_x(-mouse_delta.y * rotation_speed)
#
	## Move the camera based on WASD or arrow key input
	#var direction = Vector3()
#
	#if Input.is_action_pressed("ui_up"):
		#direction -= transform.basis.z
	#if Input.is_action_pressed("ui_down"):
		#direction += transform.basis.z
	#if Input.is_action_pressed("ui_left"):
		#direction -= transform.basis.x
	#if Input.is_action_pressed("ui_right"):
		#direction += transform.basis.x
#
	## Normalize direction to prevent faster diagonal movement
	#direction = direction.normalized()
#
	## Move the camera
	#translate(direction * move_speed * delta)
