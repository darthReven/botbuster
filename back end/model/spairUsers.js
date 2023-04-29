//Sibi Srinivas , DISM/FT/2A/01 , p2128962
const db = require("./databaseConfig");
var jwt = require("jsonwebtoken");
var config = require("../config.js");
const spairUserDB = {
  //adds a new user into the sql database. called by endpoint 1
  newUser: function (
    username,
    email,
    contact,
    password,
    Role,
    profile_pic_url,
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
          "insert into spair.users (username, email, contact, password, role, profile_pic_url) values(?, ?, ?, ?, ?, ?);";
        //execute the sql statement
        conn.query(
          sql,
          [username, email, contact, password, Role, profile_pic_url],
          function (err, result) {
            //close the connection
            conn.end();
            //if theres an error
            if (err) {
              console.log(err)
              return callback(err, null);
            }
            //
            else {
              //if after adding the new user into the database, send them a token so they can immediately log in
              token = jwt.sign(
                { id: username, role: Role },
                config.key,
                {
                  expiresIn: 86400, //expires in 24 hrs
                }
              );
              console.log("@@token " + token);
              return callback(null, token, result);
            }
          }
        );
      }
    });
  },
  //returns an array of all the existing users. called by endpoint 2
  getUsers: function (callback) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql = "Select * from spair.users"; //the reason the userid is not put into this line directly is to prevent sql injection
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
  //returns an single user whose userid is specified. called  by endpoint 3
  getUser: function (id, callback) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql = "Select * from spair.users where userid=?"; //the reason the userid is not put into this line directly is to prevent sql injection
        //execute the sql statement
        conn.query(sql, [id], function (err, result) {
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
  //updates the user's details by using the userid. called by endpoint 4
  updateUser: function (
    userid,
    username,
    email,
    contact,
    password,
    role,
    profile_pic_url,
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
          "UPDATE spair.users set username=?, email=?, contact=?, password=?, role=?, profile_pic_url=? where userid=?;";
        //execute the sql statement
        conn.query(
          sql,
          [username, email, contact, password, role, profile_pic_url, userid],
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
  loginUser: function (email, password, callback) {
    var conn = db.getConnection();

    conn.connect(function (err) {
      if (err) {
        console.log(err);
        return callback(err, null);
      } else {
        console.log("Connected!");

        var sql = "select * from users where email=? and password=?";

        conn.query(sql, [email, password], function (err, result) {
          conn.end();

          if (err) {
            console.log("Err: " + err);
            return callback(err, null, null);
          } else {
            var token = "";
            var i;
            if (result.length == 1) {
              token = jwt.sign(
                { id: result[0].userid, role: result[0].role },
                config.key,
                {
                  expiresIn: 86400, //expires in 24 hrs
                }
              );
              console.log("@@token " + token);
              return callback(null, token, result);
            } else {
              var err2 = new Error("UserID/Password does not match.");
              err2.statusCode = 500;
              return callback(err2, null, null);
            }
          } //else
        });
      }
    });
  },
};
module.exports = spairUserDB;
