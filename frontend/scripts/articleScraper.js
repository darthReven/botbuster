const request = require('request')
const axios = require('axios')
const cheerio = require('cheerio')

requestUrl = "https://www.instagram.com/";
// request(requestUrl, (error, response, html) => {
//   if (!error && response.statusCode == 200) {
//     const $ = cheerio.load(html);

//     const headings = $("h1, h2, h3, h4, h5, h6");
//     console.log(headings.text());
//   }
// });

async function scrapper() {
    const axiosResponse = await axios.request({
      method: "GET",
      url: requestUrl,
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36",
      },
    });
    // console.log(axiosResponse)
    const $ = cheerio.load(axiosResponse.data);

    const headings = $("h1, h2, h3, h4, h5, h6");
    const pagetext = $("p, a")
    console.log(headings.text());
  console.log(pagetext.text());
  console.log(html)
}
scrapper()