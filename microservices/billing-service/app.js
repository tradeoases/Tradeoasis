require("dotenv").config();
const express = require("express");
const cors = require("cors");
const cookieParser = require("cookie-parser");
const jwt = require("jsonwebtoken");
const mongoose = require("mongoose");
const webPush = require("web-push");
const socket = require("socket.io");

const app = express();

app.use(cors());
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));


const { PORT, NODE_ENV, DB_CONNECTION_STRING, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY } = process.env;

const nodeEnv = NODE_ENV || "production";
const port = PORT || 5000;
const dbURI = nodeEnv === "development" ? "mongodb://127.0.0.1:27017/tradeoasis_db_demo" : DB_CONNECTION_STRING;

mongoose.set("strictQuery", true);
mongoose
  .connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => {
    const server = app.listen(port, () => {
      console.log(`Billing Microservice is running on port ${port}`);
    });

    // Socket IO
    const io = socket(server);
    io.on("connection", (socket) => {
      console.log("Socket connection..", socket.id);

      socket.on("chat", (data) => {
        io.to(socket.id).emit("chat", { data });
      });

      // socket.on("typing", (data) => {
      //   io.sockets.emit("typing", data);
      // });
    });
  })
  .catch(() => console.log("Network connection failure!"));


webPush.setVapidDetails("mailto:web-push@foroden.com", VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY);

app.use("/", require('./src/routes/serviceRoutes'));
app.use("*", (req, res) => res.redirect("/"));




