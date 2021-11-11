# Web Scraping Project
### First project from the ITC program
Creators: Sahar G. | Bar I. | Omer C.  

Main project purpose:  
&emsp;Create an easy-to-read table of restaurants in a chosen city.  
&emsp;The table will contain information about the type of the restaurant,  
&emsp;the pricing of the restaurant, number of reviews and average review.

By using the function ```food_scraper``` you can gather information from Tripadvisor  
and insert it into said table.  
The variables of ```food_scraper``` are as follows:
* <span style="color: red">file_name</span> - The name of the csv file that will be created in the working folder.
* <span style="color: red">city</span> - Restaurants from this city will get inserted to the csv file
* <span style="color: red">first_page</span> - The page of Tripadvisor to start the scrape from
* <span style="color: red">last_page</span> - The page to finish the scrape

Fields that will be in the csv:
* <span style="color: red">Restaurant name</span>
* <span style="color: red">Rating</span> - Average review of the restaurant (0-5)
* <span style="color: red">Number of reviews</span>
* <span style="color: red">Price</span> - for now it is written in format of $ - $$$$
* <span style="color: red">Restaurant type (Cuisine)</span> - What kind of food the restaurant serves
* <span style="color: red">City rate/span> - The rank of the restaurant among all the other restaurants in the city
* <span style="color: red">Address</span> 
* <span style="color: red">Website</span> 
* <span style="color: red">Phone number</span> 