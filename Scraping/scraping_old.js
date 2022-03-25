'use strict';

const puppeteer = require('puppeteer');
const fs = require('fs');
const cheerio = require('cheerio');
const MAX_ITEMS = 500; // number of pins to extract
const MAX_NUM_FURNITURE = 100; // number big enough so its not a limitation. Implemented only for testing functionality
const PATH = 'https://www.pinterest.es/search/pins/?q=';


async function scrapeItems(page, url, scrollDelay = 800) {
    try {
        let id = url.split('?q=')[1];
        const cdp = await page.target().createCDPSession();
        let bodyHTML = await page.evaluate(() => document.documentElement.outerHTML);
        const $ = cheerio.load(bodyHTML);

        let items = [];

        let previousHeight;

        //Scroll to get MAX_ITEMS pins
        while (items.length <= MAX_ITEMS) {
            //console.log(items.length);
            $('[data-test-id="pin"]').each((idx, e) => {
                let obj = new Object({id:id});
                if(items.length > MAX_ITEMS) {return false;}
                const element = $(e);
                const link = element.find('a[href*="/pin"]');
                const title = element.find('h3');
                const image = element.find('img');

                obj.link = "https://www.pinterest.es"+link.attr('href');
                obj.image = image.attr('src');
                obj.title = title.text();
                items.push(obj);
            });
            //console.log(items.length);

            previousHeight = await page.evaluate('document.body.scrollHeight');
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
            await page.waitForFunction(`document.body.scrollHeight > ${previousHeight}`);
            await page.waitForTimeout(scrollDelay);
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
            const pws = JSON.parse($("[id='__PWS_DATA__']")[0].children[0].data);
            const resource = pws.props?.initialReduxState?.resources?.PinResource;

            if (resource != null) {
                let description = resource[Object.keys(resource)[0]].data.description;
                
                if (description == null || description == ''){
                    items[i].description = 'None';
                } else{
                    items[i].description = description;
                }
            } else{
                items[i].description = 'None';
            }

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
                let b = true;
                // sometimes followers are in other places
                $('[aria-disabled="false"][role="button"]').each((idx,e) =>{
                    followers = $(e).text();
                    if(followers.includes("seguidor")){
                        items[i].followers = followers;
                        b = false;
                    }
                    
                });
                if(b) {items[i].followers = 'None';}
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

            $('script[type="application/ld+json"]').each((idx, e) => {
                if (idx == 1 && (JSON.parse($(e).html()) == null || JSON.parse($(e).html()) == '')){
                    items[i].datePublished = 'None';
                } else if (idx == 1 && (JSON.parse($(e).html()) != null || JSON.parse($(e).html()) != '')){
                    items[i].datePublished = JSON.parse($(e).html()).datePublished;
                }
            });
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
  let data_link = fs.readFileSync("links.txt");

  data_link = data_link.toString().split("\n").slice(0,MAX_NUM_FURNITURE);

  data_link.forEach(function(line, index, arr) {
      if (index === arr.length - 1 && line === "") { return; }
      url_list.push(PATH + line.replace('\r',''));
  });

  let result = [];
  //const proxy_list = ['...','...'];
  //Search all URLs
  for (let i = 0; i < url_list.length; i++) {

      // Set up Chromium browser and page.
      const proxy = proxy_list[Math.floor(Math.random()*proxy_list.length)];

      const browser = await puppeteer.launch({headless: true, args: [proxy]});
      const page = await browser.newPage();
      page.setViewport({ width: 1280, height: 926 });

      console.log(url_list[i]);
      // Navigate to the main page.
      await page.goto(url_list[i]);
      // Auto-scroll and extract desired items from the page.
      const jsons = await scrapeItems(page, url_list[i]);

      for(const json of jsons){
          result.push(json);
      }
      // Close the browser.
      await browser.close();
  }
  // save result
  fs.writeFileSync('./items2.json', JSON.stringify(result));
})();

