extends Node

# The URL we will connect to.
@export var websocket_url = "wss://droid-osmosis-1.onrender.com"
signal end_effector_goal(json_data)

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

			var json = JSON.new()
			var error = json.parse(data)
			if error == OK:
				var json_data = json.data
				# Publish the json data for robots or other controllables to consume
				emit_signal("end_effector_goal", json_data["goals"]["right"])

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
