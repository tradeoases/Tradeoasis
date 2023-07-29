const express = require("express");
const router = express.Router();

const {someFunction} = require("../controllers/billingController");

router.get("/", someFunction);

module.exports = router;