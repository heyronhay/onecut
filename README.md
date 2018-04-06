# onecut:  Query well so you only have to cut once
Simple learning project to scrape a web api, stick data in a database, and set up an api service to query the data.

Installation:
 * Make sure Docker 17.06.1 or later is installed
 * Download the zip file ("Clone or download" button, select "Download ZIP" from popup)
 * Extract zip file
 * `cd` into directory created
 * Build docker image by running `./build-onecut-docker.sh`
 * Run docker images by running `./run-onecut-docker.sh`
 * `curl localhost:5000/` should return:
```
{
"hello_world": "onecut is live!"
}
```
 
 API Endpoint:
  * `query`:
    * Search for the given term specified by `saleterm`
    * `curl -d saleterm='kindle' localhost:5000/query` will search for all instances of "kindle"
    * Return is a json object with each hit returned like this:
    ```
        {
      "amazon_url": "https://www.amazon.com/dp/B00TD514Z8",
      "full_text": "\"Gratitude Journal\" book will be free for the next 5 days! https://t.co/sPXGFPxqu5 #kindle #free #sale #freebooks #promotion #books #freebie #discount",
      "tweet_id": "982259174754074625",
      "tweet_url": "https://twitter.com/statuses/982259174754074625"
    }
    ```
    