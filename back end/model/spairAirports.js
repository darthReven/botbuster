//Sibi Srinivas , DISM/FT/2A/01 , p2128962
const db = require("./databaseConfig");
const spairAirportsDB = {
  //adds an new airport. called by endpoint 5
  addAirport: function (name, country, description, callback) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql =
          "insert into spair.airports (name, country, description) values(?, ?, ?);"; //the reason the userid is not put into this line directly is to prevent sql injection
        //execute the sql statement
        conn.query(sql, [name, country, description], function (err, result) {
          //close the connection
          conn.end();
          if (err) {
            return callback(err, null);
          } else {
            return callback(null, result);
          }
        });
      }
    });
  },
  //returns a array of all the airports in the table data. called by endpoint 6
  getAirports: function (callback) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql = "Select * from spair.airports"; //the reason the userid is not put into this line directly is to prevent sql injection
        //execute the sql statement
        conn.query(sql, function (err, result) {
          //close the connection
          conn.end();
          if (err) {
            return callback(err, null);
          }
          //
          else {
            return callback(null, result);
          }
        });
      }
    });
  },
  // adds a new flight. used by endpoint 7
  addFlight: function (
    flightCode,
    aircraft,
    originAirport,
    destinationAirport,
    embarkDate,
    travelTime,
    price,
    callback
  ) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql =
          "insert into spair.flights (flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price) values(?, ?, ?, ?, ?, ?, ?);"; //the reason the userid is not put into this line directly is to prevent sql injection
        //execute the sql statement
        conn.query(
          sql,
          [
            flightCode,
            aircraft,
            originAirport,
            destinationAirport,
            embarkDate,
            travelTime,
            price,
          ],
          function (err, result) {
            //close the connection
            conn.end();
            if (err) {
              return callback(err, null);
            } else {
              return callback(null, result);
            }
          }
        );
      }
    });
  },
  //returns a list of flights that go from the origin airportid to the destination airportid. called by endpoint 8
  getflightDirect: function (originAirportId, destinationAirportId, callback) {
    const conn = db.getConnection();
    conn.connect(function (err) {
      if (err) {
        console.log(err);
        return callback(err, null);
      } else {
        const sql = `SELECT DISTINCT flights.flightid, flights.flightCode, flights.aircraft, (select name from spair.airports where airportid = flights.originAirport) as originAirport, (select name from spair.airports where airportid = flights.destinationAirport) AS destinationAirport, flights.embarkDate, flights.travelTime, flights.price                  FROM spair.flights, spair.airports                 WHERE originAirport=? and destinationAirport=?`;
        conn.query(
          sql,
          [originAirportId, destinationAirportId],
          (error, results) => {
            conn.end();
            if (error) {
              return callback(error, null);
            }

            return callback(null, results);
          }
        );
      }
    });
  },
  //new function to query database for a specific
  getflight: function (flightid, callback) {
    const conn = db.getConnection();
    conn.connect(function (err) {
      if (err) {
        console.log(err);
        return callback(err, null);
      } else {
        const sql = `select * from spair.flights where flightid=? `;
        conn.query(
          sql,
          [flightid],
          (error, results) => {
            conn.end();
            if (error) {
              return callback(error, null);
            }

            return callback(null, results);
          }
        );
      }
    });
  },
  //creates a new booking for a flight. called by endpoint 9
  bookFlight: function (
    userid,
    flightid,
    name,
    passport,
    nationality,
    age,
    callback
  ) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql =
          "insert into spair.bookings (name, passport, nationality, age, flightID, userid) values(?, ?, ?, ?, ?, ?);"; //the reason the userid is not put into this line directly is to prevent sql injection
        //execute the sql statement
        conn.query(
          sql,
          [name, passport, nationality, age, flightid, userid],
          function (err, result) {
            //close the connection
            conn.end();
            if (err) {
              return callback(err, null);
            }
            //
            else {
              return callback(null, result);
            }
          }
        );
      }
    });
  },
  //deltes the specified flightid. called by endpoint 10
  deleteFlight: function (flightid, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
      if (err) {
        console.log(err);
        return callback(err, null);
      } else {
        var sql = "Delete from spair.flights where flightid=?";

        conn.query(sql, [flightid], function (err, result) {
          conn.end();

          if (err) {
            console.log(err);
            return callback(err, null);
          } else {
            return callback(null, result);
          }
        });
      }
    });
  },
  //returns an array of flights that go from the origin airport to the destination airport wiht a  minumum of one transfer. called
  //by endpoint 11.
  getFlightsWithTransfer: function (
    originAirportId,
    destinationAirportId,
    callback
  ) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql = `SELECT 
                flight1.flightid as flightid1, 
                flight2.flightid as flightid2, 
                flight1.flightCode as flightCode1, 
                flight2.flightCode as flightCode2, 
                flight1.aircraft as aircraft1, 
                flight2.aircraft as aircraft2, 
                airport1.name as originAirport, 
                airport2.name as transferAirport, 
                airport3.name as destinationAirport, 
                (flight1.price + flight2.price) as "Total price"
                FROM 
                spair.flights as flight1, spair.flights as flight2, spair.airports as airport1, spair.airports as airport2, spair.airports as airport3 
                WHERE 
                airport1.airportid = flight1.originAirport 
                AND 
                    airport2.airportid = flight1.destinationAirport 
                AND 
                    airport3.airportid = flight2.destinationAirport 
                AND 
                    flight2.originAirport = flight1.destinationAirport 
                AND 
                    flight1.originAirport = ?
                AND 
                    flight2.destinationAirport = ?`;
        //execute the sql statement
        conn.query(
          sql,
          [originAirportId, destinationAirportId],
          function (err, result) {
            //close the connection
            conn.end();
            if (err) {
              return callback(err, null);
            }
            //
            else {
              return callback(null, result);
            }
          }
        );
      }
    });
  },
  getFlights: function (callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
      if (err) {
        console.log(err);
        return callback(err, null);
      } else {
        console.log("***Connected!");

        var sql = `SELECT * from flights`;

        conn.query(sql, function (err, result) {
          conn.end();
          if (err) {
            console.log(err);
            return callback(err, null);
          } else {
            return callback(null, result);
          }
        });
      }
    });
  },
};
module.exports = spairAirportsDB;
