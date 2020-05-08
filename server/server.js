const express = require('express')
var bodyParser = require('body-parser');

const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const server = require('http').Server(app);
const io = require('socket.io')(server);

server.listen(80);
// WARNING: app.listen(80) will NOT work here!
dataOrders = []

app.post('/dataOrder', (req,res) => {
    data = req.body
    console.log(data)
    dataOrders.push(data)
    res.send("ok")
})

io.on('connection', (socket) => {

});

setInterval(function () {
    if(dataOrders.length > 0){
        dataOrders.forEach(order => {
            io.sockets.emit('dataOrders', order)
        })
        dataOrders = []
    }
}, 20000);
