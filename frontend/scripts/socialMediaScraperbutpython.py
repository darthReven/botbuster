import asyncio
import pyppeteer

pageurl = "https://twitter.com/nasa"

# dictionary storing the configurations for popular websites
websiteConfigs = {
    "twitter": [
        "span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0",
        "H1"
    ],
    "reddit": [
        "H1",
        "H2",
        "H3",
        "H4"
    ]
}

# scraper
async def scrapeInfiniteScrollItems(page, contentselector, itemTargetCount):
    await asyncio.sleep(2.5)
    items = []

    while itemTargetCount > len(items):
        selectedItems = await page.evaluate('''(contentselector) => {
            const selectedItems = [];
            const elements = Array.from(document.querySelectorAll("*"));

            for (const element of elements) {
                for (const selector of contentselector) {
                    if (element.matches(selector)) {
                        selectedItems.push(element);
                        break;
                    }
                }
            }

            return selectedItems.map((item) => item.innerText);
        }''', contentselector)

        previousHeight = await page.evaluate("document.body.scrollHeight")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.waitForFunction(f'document.body.scrollHeight > {previousHeight}')
        await asyncio.sleep(1)

        items = selectedItems

    return items


# calling the scraper
async def scraper():
    browser = await pyppeteer.launch(headless=False)
    page = await browser.newPage()
    await page.goto(pageurl)

    items = await scrapeInfiniteScrollItems(page, websiteConfigs["twitter"], 5)

    print(items)
    await browser.close()


asyncio.get_event_loop().run_until_complete(scraper())