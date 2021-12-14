# Web Scraping Project
### First project from the ITC program
Creators: Sahar G. | Bar I. | Omer C.  

Main project purpose:  
&emsp;Create an easy-to-read db of restaurants in chosen cities.  
&emsp;The db will contain 5 tables: cities, restaurants, cuisines, reviews, awards.     
&emsp;See ERD below for tables contents.

By using the ```tripadvisor_scraper.py```  you can insert list of cities and number of pages per city (max 30 restaurants per page) and it will insert desired data to db tables.    
The arguments of ```tripadvisor_scraper.py``` are as follows:
* <span style="color: red">cities</span> - name of the desired cities, ```-c "city_1" "city_2"```
* <span style="color: red">pages</span> - Number of restaurants pages to scrape per city ```-p #num```
* <span style="color: red">API</span> - Optional - perform scraping using Travel Advisor API (RapidAPI) ```--API```  

 

####Initial Configuration:
 - Make sure you have Google Chrome browser installed (relevant for web scraping, not API)
 - Install requirements.txt ```pip install -r requirements.txt```
 - Edit db_config.py ```USERNAME``` and ```PASSWORD``` with local MySQL configuration
 - Edit ```HEADERS``` in config.py for Travel Advisor API based on you personal account
https://rapidapi.com/apidojo/api/travel-advisor/

Run ```tripadvisor_scraper.py -c "city_1" "city_2" etc -p #num#```

####Data which can be retrieved only via API:
- ```cities``` table - ```num_restaurants```, ```timezone```, ```num_reviews```, ```latitude```, ```longitude```
- ```restaurants``` table - ```latitude```, ```longitude```
- ```awards``` table
- ```reviews``` table - API is limited to 3 reviews per restaurant, Web scraper limited to 10.

![](WhatsApp Image 2021-12-14 at 21.45.05.jpeg)