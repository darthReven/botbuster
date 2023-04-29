// Sibi Srinivas S/O Ganesan DISM 2A 01
const app = require("./controller/app.js");
const hostname = "localhost";
const port = 8081;

//start listening for connections
app.listen(port, hostname, function () {
  console.log(`app started at http://${hostname}:${port}`);
});
