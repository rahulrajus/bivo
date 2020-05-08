var socket = require('socket.io-client')('http://localhost:80');

// WARNING: app.listen(80) will NOT work here!

socket.on('dataOrders', (data) => {
  console.log(`received dataOrder: `);
  console.log(data)
  console.log("done")
})
