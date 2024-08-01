extends Node

# The URL we will connect to.
@export var websocket_url = "wss://droid-osmosis-1.onrender.com"

# Our WebSocketClient instance.
var socket = WebSocketPeer.new()
var prev_wrist_data
var prev_positions: Dictionary

func _ready():
	# Initiate connection to the given URL.
	var err = socket.connect_to_url(websocket_url)
	if err != OK:
		print("Unable to connect")
		set_process(false)
	else:
		# Wait for the socket to connect.
		await get_tree().create_timer(2).timeout

		# Send data.
		socket.send_text("Test packet")

func _process(_delta):
	# Call this in _process or _physics_process. Data transfer and state updates
	# will only happen when calling this function.
	socket.poll()

	# get_ready_state() tells you what state the socket is in.
	var state = socket.get_ready_state()

	# WebSocketPeer.STATE_OPEN means the socket is connected and ready
	# to send and receive data.
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			var data = socket.get_packet().get_string_from_utf8()
			#print("Got data from server: ", data)
			# var robot = get_parent().get_node("GenesisArmVDroid") as CharacterBody3D

			# Simulate the action press
			var action
			# TODO: check if JSON and then parse it
			var json = JSON.new()
			var error = json.parse(data)
			if error == OK:
				var json_data = json.data
				var wrist_data
				# For the Vision controller:
				if json_data["rightHand"]:
					# Sniff test using wrist (most important)
					wrist_data = json_data["rightHand"]["jointPositions"]["forearmWrist"]
					wrist_data = _sort_dict_keys(wrist_data)

					if prev_wrist_data == null: prev_wrist_data = wrist_data
					if wrist_data != prev_wrist_data && prev_wrist_data:
						# print("wrist data", wrist_data)

						for coor in ["x", "y", "z"]:
							var diff = abs(wrist_data[coor] - prev_wrist_data[coor])
							if abs(diff) > 0.5:
								print("wrist moved {diff} on the {coor} plane: ".format({
									"diff": diff,
									"coor": coor
								}))

					# Check diffs of all joints
					var right_hand_joints = json_data["rightHand"]["jointPositions"]
					# If initially empty just copy the current joint positions
					if prev_positions.keys().size() == 0:
						prev_positions = right_hand_joints
					for joint in right_hand_joints.keys():
						for coor in ["x", "y", "z"]:
							var diff = abs(right_hand_joints[joint][coor] - prev_positions[joint][coor])
							if abs(diff) > 0.5:
								print("{joint} moved {diff} on the {coor} plane: ".format({
									"joint": joint,
									"diff": diff,
									"coor": coor
								}))

				else:
				# For the Unity Controller:
					wrist_data = json_data["RightHand"]["wrist"]
					if wrist_data != prev_wrist_data:
						print("wrist data", wrist_data)


				# Simple 2D control
				# If the wrist goes left, we want to move left
				# If the wrist goes forward, we want to move "up"
				# Note: this should really set a target position for the block
				# to move to for best sim
				if wrist_data["x"] - prev_wrist_data["x"] > 0:
					Input.action_press("ui_right", wrist_data["x"])
				else:
					Input.action_press("ui_left", wrist_data["x"])

				prev_wrist_data = wrist_data

			else:
				match data:
					# The below is used if manually driving from the CLI
					"up":
						action = "ui_up"
						Input.action_press(action, 1.0)
					"down":
						action = "ui_down"
						Input.action_press(action, 1.0)
					"left":
						action = "ui_left"
						Input.action_press(action, 1.0)
					"right":
						action = "ui_right"
						Input.action_press(action, 1.0)
					_:
						print("data did not match any case, it looked like: ", data)
						action = ""

			await get_tree().create_timer(1).timeout  # Wait for 1 second
			if action: Input.action_release(action)
			#print('Simulating action release: ', action)

	# WebSocketPeer.STATE_CLOSING means the socket is closing.
	# It is important to keep polling for a clean close.
	elif state == WebSocketPeer.STATE_CLOSING:
		pass

	# WebSocketPeer.STATE_CLOSED means the connection has fully closed.
	# It is now safe to stop polling.
	elif state == WebSocketPeer.STATE_CLOSED:
		# The code will be -1 if the disconnection was not properly notified by the remote peer.
		var code = socket.get_close_code()
		print("WebSocket closed with code: %d. Clean: %s" % [code, code != -1])
		set_process(false) # Stop processing.

func _sort_dict_keys(input_dict: Dictionary) -> Dictionary:
	var sorted_dict = {}
	var keys = input_dict.keys()
	keys.sort()

	for key in keys:
		var value = input_dict[key]
		if typeof(value) == TYPE_DICTIONARY:
			sorted_dict[key] = _sort_dict_keys(value)
		else:
			sorted_dict[key] = value

	return sorted_dict
