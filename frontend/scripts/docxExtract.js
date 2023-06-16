//extract txt frm word docs.
var mammoth = require("mammoth");
const fs = require("fs");
const pdfjsLib = require("pdfjs-dist/legacy/build/pdf.js");

var extract = {

  extractDocx: function (file) {
    var reader = new FileReader()
    reader.onload = function (event) {
      var arrayBufferFile = event.target.result;

      mammoth
        .extractRawText({ arrayBuffer: arrayBufferFile })
        .then(function (result) {
          var text = result.value; // The raw text
          //this prints all the data of docx file
          console.log(text)
          return text;
        })
        .done();
    }
    
  },

  extractPDF: function (file) {
    // const pdfPath = "./PDFExtraction/test7.pdf";

    // Load the PDF file asynchronously
    const loadingTask = pdfjsLib.getDocument(pdfPath);
    loadingTask.promise.then(async function (pdf) {
      // Get the text content of all pages
      const numPages = pdf.numPages;
      let text = "";
      for (let i = 1; i <= numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent({
          normalizeWhitespace: true,
        });

        // Extract the text strings from the text content, excluding headers, footers, and page numbers
        const textItems = textContent.items.filter(function (item) {
          // Exclude text content that falls within the top or bottom 10% of the page
          const pageHeight = page.view[3];
          const topLimit = 0.1 * pageHeight;
          const bottomLimit = 0.9 * pageHeight;
          return (
            item.transform[5] > topLimit &&
            item.transform[5] < bottomLimit &&
            item.str !== "" &&
            !item.str.match(/^\d+$/) &&
            !item.str.match(/^(page|p\.?|pp\.?)\s\d+$/i)
          );
        });

        const pageText = textItems
          .map(function (item) {
            return item.str;
          })
          .join(" ");

        text += pageText + " ";
        if (i === numPages) {
          console.log(text);
        }
      }
    });
  },

  extractTXT: function (file) {
    fs.readFile("./TXTExtraction/test.txt", "utf8", function (err, data) {
      if (err) throw err;
      console.log(data);
    });
  }
}

module.exports= extract