import datetime
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <h1>Тестовое задание<br>введите текст:</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Отправить</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('p')
                msg_json = JSON.parse(event.data)
                msg_number = msg_json['message_number']
                msg_date = msg_json['message_date']
                msg_text = msg_json['send_message']
                var content = document.createTextNode(msg_number + 
                '. Вы написали: "' + msg_text + '". Время публикации: ' + 
                msg_date)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                let message_data = {
                                  send_message: input.value,
                                };
                let json_message = JSON.stringify(message_data);
                ws.send(json_message)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    msg_number = 0
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        msg_number += 1
        msg = json.loads(data)
        msg['message_number'] = msg_number
        msg['message_date'] = datetime.datetime.now().strftime(
            '%d-%m-%Y %H:%M')
        await websocket.send_json(msg)
