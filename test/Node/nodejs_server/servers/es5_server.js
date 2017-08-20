var http = require('http');

var PORT = 8080;

function handleRequest(req, res){
    res.end(`It Works!! Path Hit:  ${req.url}`);
}

var server = http.createServer(handleRequest);

server.listen(PORT, function() {
    //Callback triggered when server is successfully listening. Hurray!
    console.log("Server listening on: http://localhost:%s", PORT);
});
