'''

# Author: Marwan Sharaf
# Date Created: 14/07/2021
# 


 Give a list of urls in a textfile, 
 Check each url on Symantec Site Review
 Scrape for:
   - Category
   - Last Time Rated
   - Risk or Not
 Return results in a CSV file
 # Note: if 5 consecutive errors take place the program will terminate

 Requirements:
 - Google Chrome
 - Install chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads)
 	#Note: Make sure it is the same version as your Chrome browser
 - Python3
 - install requests mdoule (pip3 install requests)
 - install selenium module (pip3 install selenium)
 - install pandas module   (pip3 install pandas)

 To Run:
 - Download SiteReviewScraoe.py
 - Create textfile in same folder/directory and populate with urls
 	#Note: Make sure:
 		- each url is in a seperate line
 		- Dont worry about empty lines they will be ignored
 		- change the name of the textfile in the code to its name on your machine
 - cd folder/directory path
 - python3 SiteReviewScraoe.py
 	#Note: before running make sure to change the chromedriver path in the code to its path on your machine

'''


import requests
import time
import datetime
import pandas as pd
from selenium import webdriver

urls = []
urls_used = []
search = []
category = []
lastCheck = []
risk = []

# Delay(in seconds) so website can have couple of seconds to load all its elements
# If errors occur try increasing delay
delay = 4

# Chromedriver path
# Make sure to change to path on your machine before running
chromedriver_path = '/Users/csoc/Desktop/chromedriver/chromedriver'

siteReview = 'https://sitereview.bluecoat.com/#/lookup-result/'

# Text file contianing URls
# Make sure to change the name to its name on your machine
with open("domains2.txt") as f:
	lines = (line.rstrip() for line in f)
	lines = (line for line in lines if line)
	for line in lines:
			line = line.lower()
			urls.append(line)
			line = line.replace('/', '%252F')
			line = line.replace(':', '%253A')
			search.append(siteReview + line)

urls = [x.strip() for x in urls]
search = [x.strip() for x in search]

#Pull information from Site Review
for info, url in zip(search, urls):	

	if(('Err' * 5) in ''.join(map(str, risk))):
		print('5 Consecutive Errors have occurred, program is terminating.\n')
		break
	
	urls_used.append(url)
	
	driver = webdriver.Chrome(executable_path=chromedriver_path)
	driver.get(info)

	time.sleep(delay)

	length = (len(driver.find_elements_by_xpath('//*[@id="submissionForm"]/span/span[1]/div/div[2]/span')))

	try:
		if driver.find_elements_by_xpath('//*[@id="submissionForm"]/span/span[1]/p/span[1]')[0].text == 'This URL has not yet been rated':
			
			#Pull Category
			category_element = driver.find_elements_by_xpath('//*[@id="submissionForm"]/span/span[1]/p/span[1]')[0]
			category.append(category_element.text)
			
			date = None
			lastCheck.append(date)
			
			risk_value = 'N/A'
			risk.append(risk_value)

			print('URL: {} \nCategory: {} \nLast Time Rated: {} \nRisk: {}\n '.format(url, category_element.text, date, risk_value))

	except Exception as e:
		try:
			multiCategory = []

			for loc in range(1, length):
				#Pull Category
				category_element = driver.find_elements_by_xpath('//*[@id="submissionForm"]/span/span[1]/div/div[2]/span[{}]/span'.format(loc))[0]
				multiCategory.append(category_element.text)

			category.append(multiCategory)

			#Pull Last Time Rated
			date_element = driver.find_elements_by_xpath('//*[@id="submissionForm"]/span/span[1]/div/div[2]/span[{}]/span'.format(length))[0] 
			date = date_element.text
			date = date.split(':',1)[1]
			date = date.split('?')[0]
			lastCheck.append(date)

			#Pull Risk or Not
			if driver.find_elements_by_xpath('//*[@id="submissionForm"]/span/span[1]/div/div[1]/span')[0].text == 'This URL is categorized as a security risk':
				risk_value = 'Yes'
				risk.append(risk_value)
			else:
				risk_value = 'No'
				risk.append(risk_value)

			print('URL: {} \nCategory: {} \nLast Time Rated: {} \nRisk: {}\n'.format(url, multiCategory, date, risk_value))
		
		except Exception as m:
			category_element = 'Error occurred'
			category.append(category_element)

			date = 'Err'
			lastCheck.append(date)
			
			risk_value = 'Err'
			risk.append(risk_value)
			
			print('URL: {} \nCategory: {} \nLast Time Rated: {} \nRisk: {}\n'.format(url, category_element, date, risk_value))

	
	driver.close()

category = [x for x in category if x != []]
data = {'URLs': urls_used, 'Category': category, 'Last Time Rated': lastCheck, 'Risk': risk}

print(data)

df = pd.DataFrame(data)
# Write to CSV file:
filename = "siteReview_Results" + datetime.datetime.now().strftime("%d:%m:%Y__%Hh%Mm%Ss.csv")  
df.to_csv(filename)


