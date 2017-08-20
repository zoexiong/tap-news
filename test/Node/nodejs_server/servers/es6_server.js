import http from 'http';

const PORT = 8080;

http.createServer((req, res) => {
    res.end('It Works!! Path Hit: ' + req.url);
}).listen(PORT, () => {
  console.log("Server listening on: http://localhost:%s", PORT);
});
