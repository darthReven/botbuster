import asyncio
import pyppeteer
import re



# dictionary storing the configurations for popular websites
websiteConfigs = {
    "twitter.com": ["span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0"],
    "reddit.com": ["H1", "H2", "H3", "H4"],
    "default": ["H1", "H2"]
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
                        selectedItems.push([selector, element.innerText]);
                    }
                }
            }

            return selectedItems;
        }''', contentselector)

        previousHeight = await page.evaluate("document.body.scrollHeight")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.waitForFunction(f'document.body.scrollHeight > {previousHeight}')
        await asyncio.sleep(1)

        items = selectedItems

    return items


# calling the scraper
async def scraper(websiteName, pageurl):
    browser = await pyppeteer.launch(headless=False)
    page = await browser.newPage()
    await page.goto(pageurl)

    items = await scrapeInfiniteScrollItems(page, websiteConfigs[websiteName], 5)
    # print(items)
    for item in items:
        print("Selector:", item[0])
        print("Element:", item[1])
        print()

    await browser.close()


def identifyURL(providedURL):
    keyList = list(websiteConfigs.keys())
    print(keyList)
    for i in keyList:
        x = re.search(i, providedURL)
        if x:
            return i
    return "default"

pageURL = "https://twitter.com/nasa"
website = identifyURL(pageURL)
asyncio.get_event_loop().run_until_complete(scraper(website,pageURL))
