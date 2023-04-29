//Sibi Srinivas , DISM/FT/2A/01 , p2128962
var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var urlencodedParser = bodyParser.urlencoded({ extended: false });
var cors = require("cors");
app.use(bodyParser.json()); //parse appilcation/json data
app.use(urlencodedParser);
app.options("*", cors());
app.use(cors());
//import the required modules
var spairUserDB = require('../model/spairUsers.js')
var spairAirportsDB = require('../model/spairAirports.js')
var spairPromotionsDB = require('../model/spairPromotions.js')
var verifyFn=require('../auth/verifyToken.js')


//endpoints

//first post /users/ endpoint to create an new user
app.post("/users/", (req, res) => {
    let username = req.body.username
    let email = req.body.email
    let contact = req.body.contact
    let password = req.body.password
    let role = req.body.role
    let profile_pic_url = req.body.profile_pic_url;

    spairUserDB.newUser(username, email, contact, password, role, profile_pic_url,(err, result) => {
      if (err) {
          //check the type of error
            if (err.code == "ER_DUP_ENTRY") {
                res.status(442).send()
            }
            else {
                res.status(500).send()
                // console.log(err)
            }
      } else {
        console.log(result)
        res.status(201).send(`{"userid":${result.insertId}}`);
        }
    });
});

//second endpoint, get users
app.get("/users/", verifyFn.verifyToken, verifyFn.verifyAdmin, (req, res) => {
  console.log("get all users has been requested.")
  spairUserDB.getUsers((err, result) => {
    if (err) {
      res.status(500).send();
    } else {
      //check if result is empty
      if (result == null) {
        res.status(404).send()
      }
      else {
        for (let i = 0; i < result.length; i++){
          delete result[i]["password"];
        }
        res.status(200).send(result);
      }
      
    }
  });
});

//third endpoint, get user by userid
app.get("/users/:userid/", (req, res) => {
  let userid = req.params.userid;

  spairUserDB.getUser(userid, (err, result) => {
    if (err) {
      res.status(500).send(err);
    } else {
      //check if result is empty
      if (result == null) {
        res.status(404).send();
      } else {
        delete result[0]["password"];
        res.status(200).send(result);
      }
    }
  });
});

//fouth endpoint, updating a specific user
app.put("/users/:userid/",verifyFn.verifyToken, function (req, res) {
  let userid = req.params.userid;
  let username = req.body.username;
  let email = req.body.email;
  let contact = req.body.contact;
  let password = req.body.password;
  let role = req.body.role;
  let profile_pic_url = req.body.profile_pic_url;
  console.log(profile_pic_url)
  
  console.log("received update profile.")
  spairUserDB.updateUser(userid, username, email, contact, password, role, profile_pic_url, function (err, result) {
    if (err) {
      //check the type of error
      if (err.code == "ER_DUP_ENTRY") {
        res.status(422).send();
      } else {
        res.status(500).send();
      }
    } else {
      if (result == null) {
        res.status(404).send();
      } else {
        
        res.status(204).send();
      }
      
    }
  });
});

//fifth endpoint, post airport (need admin to update)
app.post("/airport", verifyFn.verifyToken, verifyFn.verifyAdmin, function (req, res) {
  console.log("add airport requested...")
  const name = req.body.name;
  const country = req.body.country;
  const description = req.body.description;

  console.log("received an add airport operation")
  spairAirportsDB.addAirport(name, country, description, function (err, result) {
    if (err) {
      //check what type of error it is
      if (err.code == "ER_DUP_ENTRY") {
        res.status(422).send();
      } else {
        res.status(500).send();
      }
    } else {
      res.status(204).send();
    }
  });
});

//sixth endpoint, get airports
app.get("/airport", function (req, res) {
  spairAirportsDB.getAirports(function (err, result) {
    if (err) {
        res.status(500).send()
    } else {
      //check if result is empty
      if (result == null) {
        res.status(404).send();
      } else {
        res.status(200).send(result);
      }
    }
  }
  );
});

//7th endpoint, post flight
app.post("/flight/", verifyFn.verifyToken, verifyFn.verifyAdmin, function (req, res) {
  console.log("post flight requested")
  const flightCode = req.body.flightCode;
  const aircraft = req.body.aircraft;
  const originAirport = req.body.originAirport;
  const destinationAirport = req.body.destinationAirport;
  const embarkDate = req.body.embarkDate;
  const travelTime = req.body.travelTime;
  const price = req.body.price;

  spairAirportsDB.addFlight(flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price, function (err, result) {
    if (!err) {
      res.status(201).send(`{\n"flightid":"${result.insertId}\n}"`);
    } else {
      console.log(err)
      if (err.code == "ER_DUP_ENTRY") {
        res.status(422).send();
      } else {
        res.status(500).send();
      }
      
    }
  });
});

//new endpoint, get flight by id
app.get("/flight/:flightID",
  function (req, res) {
    let flightid = req.params.flightID; 
    console.log("flight details requested.")
    console.log(flightid)
    spairAirportsDB.getflight( flightid,
      function (err, result) {
        if (!err) {
          if (result == null) {
            res.status(404).send();
          } else {
            console.log("sending details");
            console.log(result);
            res.status(200).send(result);
          }
        } else {
          //check if result is empty
          console.log("error sending flight details")
          res.status(500).send()
        }
      }
    );
  }
);

//eighth endpoint,get direct flights
app.get("/flightDirect/:originAirportId/:destinationAirportId", function (req, res) {
  let originAirportId = req.params.originAirportId;
  let destinationAirportId = req.params.destinationAirportId;


  spairAirportsDB.getflightDirect(originAirportId, destinationAirportId, function (err, result) {
    if (!err) {

      if (result == null) {
        res.status(404).send();
      } else {
        res.status(200).send(result);
      }
    } else {
      //check if result is empty
      res.status(500).send()
    }
  });
});


//9th endpoint, booking a flight
app.post("/booking/:userid/:flightid", function (req, res) {
  let userid = req.params.userid;
  let flightid = req.params.flightid;
  let name = req.body.name
  let passport = req.body.passport
  let nationality = req.body.nationality
  let age = req.body.age

  spairAirportsDB.bookFlight(userid, flightid, name, passport, nationality, age, function (err, result) {
    if (!err) {
      res.status(201).send(`{\n"bookingid":"${result.insertId}\n}"`);
    } else {
      res.status(500).send();
    }
  });
});

//10th endpoint 
app.delete("/flight/:id", function (req, res) {
  var flightid = req.params.id;

  spairAirportsDB.deleteFlight(flightid, function (err, result) {
    if (!err) {
      res.status(200).send('{"Message": "Deletion successful"}');
    } else {
      res.status(500).send();
    }
  });
});

//11th endpoint 
app.get("/transfer/flight/:originAirportId/:destinationAirportId", function (req, res) {
  let originAirportId = req.params.originAirportId;
  let destinationAirportId = req.params.destinationAirportId;

  spairAirportsDB.getFlightsWithTransfer(originAirportId, destinationAirportId,  function (err, result) {
    if (!err) {
      res.status(201).send(result);
    } else {
      //check if result is empty
      if (result == null) {
        res.status(404).send();
      } else {
        res.status(200).send(result);
      }
    }
  });
});

//advanced features endpoints

//create a new promotion, post /promotions/:flightid
app.post("/promotions/:flightid", verifyFn.verifyToken, verifyFn.verifyAdmin, function (req, res) {
  console.log("add promotion requested.")
  const flightid = req.params.flightid;
  const promotionPeriod = req.body.promotionPeriod;
  const discount = req.body.discount;
  const flightCode=req.body.flightCode

  spairPromotionsDB.addPromotion(flightid, promotionPeriod, discount,flightCode, function (err, result) {
    if (!err) {
      res.status(201).send(`{\n"promotionid":"${result.insertId}\n}"`);
    } else {
      res.status(500).send();
    }
  });
});


//second advanced endpoint, getting all promotions
app.get("/promotions/", function (req, res) {
  spairPromotionsDB.getPromotions(function (err, result) {
    if (!err) {
      //check if result is empty
      if (result == null) {
        res.status(404).send();
      } else {
        res.status(200).send(result);
      }
    } else {
      console.log(err)
      res.status(500).send(err);
    }
  });
});

//third advanced endpoint, getting a specific promotion by id
app.get("/promotions/:promotionid", function (req, res) {
  let promotionid = req.params.promotionid;

  spairPromotionsDB.getPromotion(promotionid, function (err, result) {
    if (!err) {
      //check if result is empty
      if (result == null) {
        res.status(404).send();
      } else {
        res.status(200).send(result);
      }
    } else {
      res.status(500).send(err);
    }
  });
});

//fouth advanced endpoint, deleting a promotion by id
app.delete("/promotions/:promotionid", function (req, res) {
  var promotionid = req.params.promotionid;

  spairPromotionsDB.deletePromotion(promotionid, function (err, result) {
    if (!err) {
      if (result == null) {
        res.status(404).send()
      } else {
        res.status(200).send('{"Message": "Deletion successful"}');
      }
      
    } else {
      console.log(err);

      res.status(500).send("Some error");
    }
  });
});

// any new endpoints from CA1 have been added below this line.

//return all fligths in the database.
app.get("/flights/", function (req, res) {
  spairAirportsDB.getFlights(function (err, result) {
    if (!err) {
      res.status(200).send(result);
    } else {
      console.log(err);
      res.status(500).send(err);
    }
  });
});

//login endpoint. this endpoint allows users to login, authenticates them and returns and web token
app.post("/user/login", function (req, res) {
  var email = req.body.email;
  var password = req.body.password;

  spairUserDB.loginUser(email, password, function (err, token, result) {
    if (!err) {
      res.statusCode = 200;
      res.setHeader("Content-Type", "application/json");
      delete result[0]["password"]; //clear the password in json data, do not send back to client
      console.log(result);
      res.json({
        success: true,
        UserData: JSON.stringify(result),
        token: token,
        status: "You are successfully logged in!",
        role: result[0].role,
        // userData: result[0]
      });
      res.send();
    } else {
      console.log(err);
      res.status(500);
      res.send(err.statusCode);
    }
  });
}); 

//search for flight by origin, destination and emabark/return date

module.exports =app