const e = require("express");
const jwt = require("jsonwebtoken");
const config = require("../config");
const verifyFn = {
  verifyToken: function (req, res, next) {
    // console.log(req.headers);

    //retrieve authorization header content
    const authHeader = req.headers["authorization"];
    console.log(authHeader);

    //check content in authoriazation header
    if (!authHeader || !authHeader.includes("Bearer")) {
      res.status(403);
      return res.send({ auth: "false", message: "AuthHeader Error" });
    } else {
      let token = authHeader.replace("Bearer ", "");
      // token=JSON.stringify(token)
      console.log(token);
      //verifying the token
      jwt.verify(token, config.key, function (err, payLoad) {
        if (err) {
          res.status(403);
          console.log("access denied at token verification")
          console.log(err)
          return res.send({ auth: "false", message: "Verify failed" });
        } else {
          req.payLoad = payLoad;
          next();
        }
      });
    }
  },
  verifyAdmin: function (req, res, next) {
    if (req.payLoad.role == "admin") {
      next();
      console.log("admin detected. allowing access...")
    } else {
      res.status(403);
      console.log("Unauthorized access detected. access denied.")
      return res.send({ auth: "false", message: "Not an Admin!" });
    }
  },
};
module.exports = verifyFn;
