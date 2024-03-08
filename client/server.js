const host = require("ip");
const http = require("http");
const path = require("path");
const express = require("express");
const compression = require("compression");

const port = 5173;
const hostname = host.address();

const app = express();

app.use(compression());
app.use(express.static(__dirname + "/dist"));

app.get("/*", (req, res) => {
  res.sendFile(path.join(__dirname + "/dist/index.html"));
});

const server = http.createServer(app).listen(port, "0.0.0.0", () => {
  console.log("URL: http://localhost:%s", port);
  console.log("URL: http://%s:%s", hostname, port);
});
