// const express = require('express')
// const app = express()
// const port = 8000


// app.get('/', (req, res) => {
// 	res.send('Hello World Cyberskill')
// })

// app.get('/user', (req, res) => {
// 	res.send('Tran Thi')
// })

// app.listen(port, () => {
//  	console.log("Listening on port 4000 ...")//
// })

const express = require("express");
const { createLogger, format, transports } = require("winston");
const LokiTransport = require("winston-loki");

const app = express();
const port = 8000;


const logger = createLogger({
  level: "info",
  format: format.combine(
    format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }), 
    format.json() 
  ),
  transports: [
    new LokiTransport({
      host: "http://139.180.158.237:3100",
      interval: 5,
      labels: { job: "nodejs" }, 
    }),
    new transports.Console(),
  ],
});


app.use((req, res, next) => {
  logger.info({
    message: `Received request: ${req.method} ${req.url}`,
    labels: { route: req.url, method: req.method },
  });
  next();
});


app.get("/", (req, res) => {
  res.send("Hello World Cyberskill");
  logger.info({
    message: "Responded to / route",
    labels: { route: "/", status: 200 },
  });
});

app.get("/user", (req, res) => {
  res.send("Tran Thi");
  logger.info({
    message: "Responded to /user route",
    labels: { route: "/user", status: 200 },
  });
});


app.use((req, res, next) => {
  const errorMessage = `Route not found: ${req.method} ${req.url}`;
  logger.error({
    message: errorMessage,
    labels: { route: req.url, method: req.method, status: 404 },
  });
  res.status(404).send("Route not found!");
});


app.use((err, req, res, next) => {
  logger.error({
    message: `Server error: ${err.message}`,
    labels: { route: req.url, method: req.method, status: 500 },
  });
  res.status(500).send("Internal server error!");
});

// Start server
app.listen(port, () => {
  logger.info({
    message: `Server started on port ${port}`,
    labels: { event: "startup" },
  });
});
