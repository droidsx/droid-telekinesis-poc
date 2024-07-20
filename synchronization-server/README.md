You can test out your web socket connection by the following:

```bash
pip install websockets
python sync_server.py
```

Create an Ngrok tunnel to your locally running server so you can connect to it over the web following setup instructions here https://dashboard.ngrok.com/get-started/setup/macos.

Run sync server and create an ngrok tunnel for it i.e.
`ngrok http http://localhost:8765`

Now, when you make a socket connection it should get forwarded by ngrok to the `sync_server` on localhost.

You can validate your setup by changing the URI in `python client.py` to whatever your URL is for ngrok. Whatever you type into the command line should get echoed back to you.
