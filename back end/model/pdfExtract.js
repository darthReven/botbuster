const fs = require('fs');
const pdfjsLib = require('pdfjs-dist/legacy/build/pdf.js');

const pdfPath = './PDFExtraction/test3.pdf';

// Load the PDF file asynchronously
const loadingTask = pdfjsLib.getDocument(pdfPath);
loadingTask.promise.then(function(pdf) {
  // Get the text content of all pages
  const numPages = pdf.numPages;
  let text = '';
  for (let i = 1; i <= numPages; i++) {
    pdf.getPage(i).then(function(page) {
      page.getTextContent({ normalizeWhitespace: true }).then(function(textContent) {
        // Extract the text strings from the text content
        const textItems = textContent.items;
        const pageText = textItems.map(function(item) {
          return item.str;
        }).join(' ');

        text += pageText + ' ';
        if (i === numPages) {
          console.log(text);
        }
      });
    });
  }
});
