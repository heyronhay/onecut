# onecut:  Query well so you only have to cut once
Simple learning project to scrape a web api, stick data in a database, and set up an api service to query the data.

* Santization (redis doesn't suffer from injection attacks)
* Authentication (Bad Ron!)
* Minimal cleanup
* Common words allowed, but not 1 letter "words"
* Only use simple Flask HTTP server
* Only english tweets that have amazon links and the word "sale" in them
* Not API versioning
* No transactions for adding tweet data
