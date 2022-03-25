'use strict';

const puppeteer = require('puppeteer');
const fs = require('fs');
const cheerio = require('cheerio');
const MAX_ITEMS = 500; // number of pins to extract
const MAX_NUM_FURNITURE = 100; // number big enough so its not a limitation. Implemented only for testing functionality
const PATH = 'https://www.pinterest.es/search/pins/?q=';


async function scrapeItems(page, url, scrollDelay = 800) {
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
            try {
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
            if (date == null || date === ''){
                items[i].date = 'None';
            } else{
                items[i].date = date;
            }
            if (items[i].datePublished == null) {
                items[i].datePublished = 'None';
            }
            $('script[type="application/ld+json"]').each((idx, e) => {
                const parsed = JSON.parse($(e).html());
                if (parsed != null && parsed["@type"] === "SocialMediaPosting") {
                    items[i].datePublished = parsed.datePublished;
                    if (parsed.author != null) {
                        items[i].authorName = parsed.author.name;
                        items[i].authorProfile = parsed.author.url
                    }
                    if (items[i].description?.trim() === "") {
                        items[i].description = parsed.articleBody;
                    }
                }
            });
            }   catch(e) {
                console.error(e);
                items[i] = null;
            }
        }
        const filtered = items.filter(i => i != null);
        if (filtered.length < items.length * 0.5) {
            throw new Error("More than half of the items could not be extracted");
        }
        return filtered;
}

(async () => {

  //get all URLS from file
  let data_link = fs.readFileSync("links.txt");

  data_link = data_link.toString().split("\n") // .slice(0,MAX_NUM_FURNITURE);

  const proxy_list =fs.existsSync("./proxies.json") ? JSON.parse(fs.readFileSync("./proxies.json")): [];
  //Search all URLs
  for (let i = 0; i < data_link.length; i++) {
      const line = data_link[i];
      if (line === "") { continue; }
      const file_name = `./items/${line}.${Math.floor(Date.now()/(24*60*60*1000))}.json`;
      if (fs.existsSync(file_name)) {
          continue;
      }
      // Create the empty file so that it will be skipped if run un parallel
      fs.writeFileSync(file_name, '[]');

      // Compute the URL
      const url = PATH + line.replace('\r','');

      // Set up Chromium browser and page.
      let browser, parsedProxy = null;
      if (proxy_list.length > 0) {
          const proxy = proxy_list[Math.floor(Math.random() * proxy_list.length)];
          parsedProxy = new URL(proxy);
          browser = await puppeteer.launch({
              headless: true, args: [
                  '--no-sandbox', `--proxy-server=${parsedProxy.hostname}:${parsedProxy.port}`,
              ]
          });
      } else {
          browser = await puppeteer.launch({
              headless: true, args: ['--no-sandbox', ] });
      }

      const page = await browser.newPage();
      if (parsedProxy != null) {
          await page.authenticate({ username: parsedProxy.username, password: parsedProxy.password });
      }
      await page.setViewport({ width: 1280, height: 926 });


      console.log(url);
      // Navigate to the main page.
      await page.goto(url);
      // Auto-scroll and extract desired items from the page.
      const jsons = await scrapeItems(page, url);
      // Close the browser.
      await browser.close();
      // save result
      fs.writeFileSync(file_name, JSON.stringify(jsons));
  }
})();

