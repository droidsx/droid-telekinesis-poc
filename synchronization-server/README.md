You can test out your web socket connection by the following:

```bash
pip install websockets
python sync_server.py
```

Create an Ngrok tunnel to your locally running server so you can connect to it over the web following setup instructions here https://dashboard.ngrok.com/get-started/setup/macos.

Run sync server and create an ngrok tunnel for it i.e.
`ngrok http http://localhost:8765`
