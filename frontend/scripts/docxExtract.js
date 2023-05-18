//extract txt frm word docs.
var mammoth = require("mammoth");

function extractDocx() {
  mammoth
    .extractRawText({ path: "SPIM.docx" })
    .then(function (result) {
      var text = result.value; // The raw text

      //this prints all the data of docx file
      console.log(text);
      var messages = result.messages;
    })
    .done();
}

module.exports = extractDocx()