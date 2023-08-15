require("dotenv").config();
// const SomeModel = require("../models/SomeModel");


const someFunction = (req, res) => {
  res.json({"success": true});
};

module.exports = {
    someFunction,
};