extends Node

# The URL we will connect to.
@export var websocket_url = "wss://droid-osmosis-1.onrender.com"
signal end_effector_goal(json_data)

# Our WebSocketClient instance.
var socket = WebSocketPeer.new()
var reconnect_attempts = 0
var max_reconnect_attempts = 10
var reconnect_delay = 0.1 # Time in seconds between reconnection attempts


func _ready():
	connect_to_websocket()


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
				if json_data && json_data.get("goals") && json_data["goals"].get("right"):
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
		reconnect()


func connect_to_websocket():
	print("Attempting to connect...")
	var err = socket.connect_to_url(websocket_url)
	if err != OK:
		print("Unable to connect")
		reconnect()
	else:
		print('Connected')
		set_process(true)


func reconnect():
	if reconnect_attempts < max_reconnect_attempts:
		reconnect_attempts += 1
		print("Reconnection attempt %d/%d" % [reconnect_attempts, max_reconnect_attempts])
		await get_tree().create_timer(reconnect_delay).timeout
		connect_to_websocket()
	else:
		print("Max reconnection attempts reached. Giving up.")

func sort_dict_keys(input_dict: Dictionary) -> Dictionary:
	var sorted_dict = {}
	var keys = input_dict.keys()
	keys.sort()

	for key in keys:
		var value = input_dict[key]
		if typeof(value) == TYPE_DICTIONARY:
			sorted_dict[key] = sort_dict_keys(value)
		else:
			sorted_dict[key] = value

	return sorted_dict
