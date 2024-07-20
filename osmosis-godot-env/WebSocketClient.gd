extends Node

# The URL we will connect to.
@export var websocket_url = "ws://localhost:8765"

# Our WebSocketClient instance.
var socket = WebSocketPeer.new()

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
			print("Got data from server: ", data)
			var robot = get_parent().get_node("GenesisArmVDroid") as CharacterBody3D

			# Simulate the action press
			var action
			match data:
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
					action = ""

			await get_tree().create_timer(1).timeout  # Wait for 1 second
			Input.action_release(action)
			print('Simulating action release: ', action)

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
