//Sibi Srinivas S/O Ganesan , DISM 2A 01.
//this file contains the functions that call the sql database for the promotions advanced features.
const db = require("./databaseConfig");
const spairPromotionsDB = {
  //function for the first advanced feature endpoint, post /promotions/:flightid
  addPromotion: function (flightid, promotionPeriod, discount,flightCode, callback) {
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
          "insert into spair.promotions (flightid, promotion_period, discount, flightCode) values(?, ?, ?, ?);"; //the reason the userid is not put into this line directly is to prevent sql injection
        //execute the sql statement
        conn.query(
          sql,
          [flightid, promotionPeriod, discount, flightCode],
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
  getPromotions: function (callback) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql = "Select * from spair.promotions"; //the reason the userid is not put into this line directly is to prevent sql injection
        //execute the sql statement
        conn.query(sql, function (err, result) {
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
  getPromotion: function (id, callback) {
    const conn = db.getConnection();
    //do a connection to the database
    conn.connect((err) => {
      //if connection fails
      if (err) {
        return callback(err, null);
      }
      //if connection successful
      else {
        const sql = "Select * from spair.promotions where promotionid=?"; //the reason the userid is not put into this line directly is to prevent sql injection
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
  deletePromotion: function (promotionid, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
      if (err) {
        console.log(err);
        return callback(err, null);
      } else {

        var sql = "Delete from spair.promotions where promotionid=?";

        conn.query(sql, [promotionid], function (err, result) {
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
module.exports = spairPromotionsDB