import asyncio
import pyppeteer
import re

# dictionary storing the configurations for popular websites
websiteConfigs = {
    "twitter.com": ["","span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0",""],
    "reddit.com": ["","H1", "H2", "H3", "H4"],
    "facebook.com": ["div.xc9qbxq","div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a"],
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
                        selectedItems.push([selector.split('.')[0], element.innerText]);
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

async def delPopUp(page,websitename):
    # await page.waitForSelector(websiteConfigs[websitename][0], {'visible': True})
    # await page.click(websiteConfigs[websitename][0])
    # print("after clicking")
    # div.x1i10hfl.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xc9qbxq.x14qfxbe.x1qhmfi1
    try:
        # Replace the CSS selector with the appropriate selector for the pop-up element
        await page.waitForSelector(websiteConfigs[websitename][0], {'timeout': 5000})
        await page.click(websiteConfigs[websitename][0])
        await page.waitForSelector(websiteConfigs[websitename][0], {'hidden': True, 'timeout': 5000})
    except pyppeteer.errors.TimeoutError:
        pass  # Pop-up not found or already closed


# calling the scraper
async def scraper(websiteName, pageurl):
    browser = await pyppeteer.launch(headless=False)
    page = await browser.newPage()
    await page.goto(pageurl)

    await delPopUp(page,websiteName)
    print('calling scroller')
    items = await scrapeInfiniteScrollItems(page, websiteConfigs[websiteName], 5)
    await browser.close()


def identifyURLSMS(providedURL):
    keyList = list(websiteConfigs.keys())
    for i in keyList:
        x = re.search(i, providedURL)
        if x:
            return i
    return "default"

