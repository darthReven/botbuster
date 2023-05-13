const fs = require("fs");
const puppeteer = require("puppeteer");

const scrapeInfiniteScrollItems = async (page, itemTargetCount) => {
  await new Promise((resolve) => setTimeout(resolve, 2000));
  let items = [];

  while (itemTargetCount > items.length) {
    items = await page.evaluate(() => {
      const items = Array.from(
        document.querySelectorAll("#id__b5wder1wfaf > span:nth-child(1)")
      );
      return items.map((item) => item.innerText);
    });

    previousHeight = await page.evaluate("document.body.scrollHeight");
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
    await page.waitForFunction(
      `document.body.scrollHeight > ${previousHeight}`
    );
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  return items;
};

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });

  const page = await browser.newPage();
  await page.goto("https://twitter.com/nasa");

  const items = await scrapeInfiniteScrollItems(page, 5);
  // const items2 = await scrapeInfiniteScrollItems(page, 10);

  console.log(items);
  // for (var i = 0; i < items.length; i++){
  //   console.log(items[i])
  // }
  browser.close();
  // console.log(items2)
})();

//https://github.com/michaelkitas/Nodejs-Puppeteer-Tutorial/blob/master/infinite_scrolling.js
