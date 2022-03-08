'use strict';

const puppeteer = require('puppeteer');
const fs = require('fs');
const cheerio = require('cheerio');
const MAX_ITEMS = 50
const URL = 'https://www.pinterest.es/search/pins/?q=chaise%20longue'


async function scrapeItems(page, itemCount, scrollDelay = 800) {
    try {
        const cdp = await page.target().createCDPSession();
        let bodyHTML = await page.evaluate(() => document.documentElement.outerHTML);
        const $ = cheerio.load(bodyHTML);

        let items = [];

        let previousHeight;

        //Scroll to get MAX_ITEMS pins
        while (items.length <= itemCount) {

            $('[data-test-id="pin"]').each((idx, e) => {
                if(items.length > itemCount) {return false;}
                const element = $(e);
                const link = element.find('a[href*="/pin"]');
                const title = element.find('h3');
                const image = element.find('img');

                items.push(["https://www.pinterest.es"+link.attr('href'), image.attr('src'), title.text()]);
            });

            previousHeight = await page.evaluate('document.body.scrollHeight');
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
            await page.waitForFunction(`document.body.scrollHeight > ${previousHeight}`);
            await page.waitForTimeout(scrollDelay);
        }

        //Enter in every pin to get more info
        for (let i = 0; i < items.length; i++) {
            const url = items[i][0];
            await page.goto(url);

            let bodyHTML2 = await page.evaluate(() => document.documentElement.outerHTML);

            const $ = cheerio.load(bodyHTML2);

            $('[data-test-id="CloseupMainPin"]').each((idx, e) => {

                const element = $(e);
                const image = element.find('img');
                items[i].push(image.attr('alt')); //Mas informacion (opcional) + pins asociats

            });
        }
        return items;
    } catch(e) { }
}

(async () => {
  // Set up Chromium browser and page.
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  page.setViewport({ width: 1280, height: 926 });

  // Navigate to the example page.
  await page.goto(URL);

  // Auto-scroll and extract desired items from the page. Currently set to extract ten items.
  const result = await scrapeItems(page, MAX_ITEMS);

  // Save extracted items to a new file.
  fs.writeFileSync('./items.txt', result.join('\n') + '\n');

  // Close the browser.
  await browser.close();
})();
