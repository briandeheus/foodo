const WebSocketServer = require('websocket').server;
const http            = require('http');
const redis           = require('redis');

const server = http.createServer((request, response) => {

    response.writeHead(200);
    response.end();

});

const wsServer = new WebSocketServer({
    httpServer: server,
    autoAcceptConnections: false
});

server.listen({'host': '0.0.0.0', port: 8000}, () => {

    console.log('Server is listening');

});

wsServer.on('request', (request) => {

    console.log('New request =>', request);

    const connection  = request.accept();
    const redisClient = redis.createClient({host: process.env['REDIS_HOST'] || 'localhost'});

    const subscribe = (listId) => {

        console.log('Subscribing to', listId);
        redisClient.subscribe(listId);

    };

    redisClient.on('message', (_, msg) => {

        connection.send(msg);

    });

    connection.on('message', function (message) {

        console.log('msg =>', message.utf8Data);

        try {

            message = JSON.parse(message.utf8Data);

        } catch (e) {

            console.error('Invalid message. Bye client.');
            connection.close();

        }

        const {cmd, listId} = message;

        switch (cmd) {

        case 'subscribe':
            subscribe(listId);
            break;

        default:
            console.log('Invalid command:', cmd);
            connection.close();
            break;

        }

    });

    connection.on('close', function (reasonCode, description) {

        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');

    });

    const int = setInterval(() => {

        if (connection.connected === false) {

            console.log(connection.remoteAddress, 'is closed. Bye');
            clearInterval(int);
            return;

        }

        console.log('pinging', connection.remoteAddress );
        connection.send(`ping:${Date.now()}`);

    }, 5000);

});
