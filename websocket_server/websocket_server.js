const WebSocketServer = require('ws');

const wss = new WebSocketServer.Server({ port: 9000 })

wss.on("connection", ws => {
    ws.on("message", data => {
        console.log(data.toString());
    });

    ws.on("close", () => {});

    ws.onerror = function () {}
});

console.log("The WebSocketServer is running on port 9000");