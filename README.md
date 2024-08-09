Osmosis is the process of syncing your hand as the leader for an arbitrary Droid so that you can record training examples.

It is similar to those corny scenes from TV where a guy shows a gal how to swing a golf club. But for Droids.

Osmosis needs the following:

- an assimilated Droid compliant with DroidOS
- a client to capture hand pose information
- middleware to convert hand information into controls

To setup up the application we create a synchronization server, connect the hand capture client to the sync server, and connect the DroidOS client.

Then we begin streaming pose information from the capture client. We should see the movement of the Droid mirror the movement of our hand.

In the future the godot environment can be completely removed as a dependency. Osmosis should not depend on a capture environment.

# API Contracts

From the hand client we expect a JSON blob with a name of the joint to the Vector3D position of each joint and/or the difference from the last observed joint.

From the DroidOS client we expect to see the sensor information returned. It should be a continuous stream of camera data, motor joint angles, and basic connection/state meta data.

The goal is to end with a series of hand positions transforms (input) and the video and other sensor data (outputs) to train our models with.

## Hand Client

Outgoing stream:

```javascript
{
    syncId: ... // sequence order each synced message
    timestamp: datetimeUTC // allows us to calculate delta
    root: Vector3D
    thumbBase: Vector3D
    thumbMid: Vector3D
    thumbTip: Vector3D
    ...
}
```

Incoming stream:

```javascript
{
  terminate: bool
}
```

## DroidOS

TODO: figure out how/where to stream sensor data, I actually don't need to receive it for now since I can directly observe it and save it locally

Outgoing stream:

```javascript
{
    <sensorName>: {
        id: uuid
        dataType: JSON | XYZVideoEncoding | Audio
        frameData: ... // proprioception data, video, other..? May need smarter ways of doing this not sure we can stream video as json blob or if it is a good idea
    }
}
```

# Steps to Run

`python sync_server.py`
`python client.py`
Run godot scene.

Type in the repl of the client.py terminal and see the text come through in the console in Godot.
