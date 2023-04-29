const fs = require('fs');

fs.readFile('./TXTExtraction/test.txt', 'utf8', function(err, data) {
  if (err) throw err;
  console.log(data);
});