const fs = require("fs");
const puppeteer = require("puppeteer");
const pageurl = "https://twitter.com/nasa";

// dictionary storing the configurations for popular websites
var websiteConfigs = {
  twitter: ["span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0", "H1"],
  reddit: ["H1", "H2", "H3", "H4"],
};

// scraper
const scrapeInfiniteScrollItems = async (page, configs, itemTargetCount) => {
  await new Promise((resolve) => setTimeout(resolve, 2500));
  let items = [];

  while (itemTargetCount > items.length) {
    items = await page.evaluate((configs) => {
      const selectedItems = [];

      const elements = Array.from(document.querySelectorAll("*"));

      for (const element of elements) {
        for (const selector of configs["twitter"]) {
          if (element.matches(selector)) {
            selectedItems.push(element);
            break;
          }
        }
      }

      return selectedItems.map((item) => item.innerText);
    }, configs);

    previousHeight = await page.evaluate("document.body.scrollHeight");
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
    await page.waitForFunction(
      `document.body.scrollHeight > ${previousHeight}`
    );
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  return items;
};

// calling the scraper
(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });

  const page = await browser.newPage();
  await page.goto(pageurl);

  const items = await scrapeInfiniteScrollItems(page, websiteConfigs, 5);

  console.log(items);
  browser.close();
})();
