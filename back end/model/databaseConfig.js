const mysql = require("mysql");

const dbconnect = {
  getConnection: () => {
    return mysql.createConnection({
      host: "localhost",
      user: "root",
      password: "1Qwer$#@!",
      database: "spair",
    });
  },
};

module.exports = dbconnect;
