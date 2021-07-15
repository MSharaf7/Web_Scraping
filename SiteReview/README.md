
# Site Review Web Scrapping 
  
  Give a list of urls in a textfile, the program will heck each url on Symantec Site Review
  
  It will Scrape for:
   - Category
   - Last Time Rated
   - Risk or Not
  
  and return results in a CSV file
 
        If 5 consecutive errors take place the program will terminate

 ## Requirements:
 - Google Chrome
 - Install chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads)
 	        
          Make sure it is the same version as your Chrome browser
 - Python3
 - install requests mdoule (pip3 install requests)
 - install selenium module (pip3 install selenium)
 - install pandas module   (pip3 install pandas)

 ## To Run:
 - Download SiteReviewScrape.py
 - Create textfile in same folder/directory and populate with urls
 	
        Make sure:
 		- each url is in a seperate line
 		- change the name of the textfile in the code to its name on your machine
 - cd folder/directory path
 - python3 SiteReviewScraoe.py

         Before running make sure to change the chromedriver path in the code to its path on your machine
