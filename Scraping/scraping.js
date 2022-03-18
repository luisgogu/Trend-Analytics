'use strict';

const puppeteer = require('puppeteer');
const fs = require('fs');
const cheerio = require('cheerio');
const MAX_ITEMS = 5;
const PATH = 'https://www.pinterest.es/search/pins/?q=';


async function scrapeItems(page, itemCount, scrollDelay = 800) {
    try {
        const cdp = await page.target().createCDPSession();
        let bodyHTML = await page.evaluate(() => document.documentElement.outerHTML);
        const $ = cheerio.load(bodyHTML);

        let items = [];

        let previousHeight;

        //Scroll to get MAX_ITEMS pins
        while (items.length <= itemCount) {
            console.log(items.length);
            $('[data-test-id="pin"]').each((idx, e) => {
                let obj = new Object();
                if(items.length > itemCount) {return false;}
                const element = $(e);
                const link = element.find('a[href*="/pin"]');
                const title = element.find('h3');
                const image = element.find('img');

                obj.link = "https://www.pinterest.es"+link.attr('href');
                obj.image = image.attr('src');
                obj.title = title.text();
                items.push(obj);
            });

            previousHeight = await page.evaluate('document.body.scrollHeight');
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
            await page.waitForFunction(`document.body.scrollHeight > ${previousHeight}`);
            await page.waitForTimeout(scrollDelay);
            console.log(items.length);
        }

        //Enter in every pin to get more info
        for (let i = 0; i < items.length; i++) {
            const url = items[i]['link'];
            await page.goto(url);

            let bodyHTML2 = await page.evaluate(() => document.documentElement.outerHTML);

            const $ = cheerio.load(bodyHTML2);

            //tags associats
            let tags = []
            $('[data-test-id="vase-tag"] > span').each((idx, e) =>{
                const element = $(e);
                tags.push(element.text());
            });
            items[i].tags = tags;

            // descripcio closeup
            // const pws = JSON.parse($("#__PWS_DATA__").text());
            // const resource = pws.props?.initialReduxState?.resources?.PinResource;
            // if (resource != null) {
            //     description = resource[Object.keys(resource)[0]].data.description;
            //
            //     if (description == null || description == ''){
            //         items[i].description = 'None';
            //     } else{
            //         items[i].description = description;
            //     }
            // }

            //descripcio oculta
            let description2 = $('meta[property="description"]').attr('content');
            if (description2 == null || description2 == ''){
                items[i].description2 = 'None';
            } else{
                items[i].description2 = description2;
            }

            //seguidors
            let followers = $('[data-test-id="official-user-attribution"] > div:nth-child(2) :nth-child(2)').text();
            if (followers == null || followers == ''){
                items[i].followers = 'None';
            } else{
                items[i].followers = followers;
            }

            //data
            let date = $('meta[property="og:updated_time"]').attr('content');
            if (date == null || date == ''){
                items[i].date = 'None';
            } else{
                items[i].date = date;
            }

            const ldJSONs = [];
            $('script[type="application/ld+json"]').each((idx, e) => {
                console.log($(e).html());
                ldJSONs.push(JSON.parse($(e).html())[1].datePublished);
            });
            console.log(ldJSONs);

        }
        return items;
    } catch(e) {
        console.error(e);
        return [];
    }
}

(async () => {

  let url_list = [];

  //get all URLS from file
  const data_link = fs.readFileSync("links.txt");

  data_link.toString().split("\n").forEach(function(line, index, arr) {
      if (index === arr.length - 1 && line === "") { return; }
      url_list.push(PATH + line.replace('\r',''));
  });

  let result = [];
  //const proxy_list = ['',..]
  //Search all URLs
  for (let i = 0; i < url_list.length; i++) {

      // Set up Chromium browser and page.
      const browser = await puppeteer.launch({headless: false, args: []});
      const page = await browser.newPage();
      page.setViewport({ width: 1280, height: 926 });

      console.log(url_list[i]);
      // Navigate to the main page.
      await page.goto(url_list[i]);
      // Auto-scroll and extract desired items from the page.
      const jsons = await scrapeItems(page, MAX_ITEMS);

      for(const json of jsons){
          result.push(json);
      }
      // Close the browser.
      await browser.close();
  }
  // save result
  fs.writeFileSync('./items.json', JSON.stringify(result));
})();

