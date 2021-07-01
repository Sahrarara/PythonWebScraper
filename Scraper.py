from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


print('Program has started')

opts = FirefoxOptions()
opts.add_argument("--headless")

driver = webdriver.Firefox(options=opts)
driver.get('https://www.wko.at/service/neuzugaenge.html')
print('WKO website has been opened')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cookieagree"))) 	#accepts the cookies popup
cookie_button = driver.find_element_by_class_name('cookieagree').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-success')))	
location = driver.find_element_by_xpath('//input[@value="w"]')						#presses the "Wien" radio button
search = WebDriverWait(driver, 3)
location.click()
print('dang popup windows, I swear')
WebDriverWait(driver,3)
search_form = driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[3]/button').click()	#clicks the dropdown box and presses the search button
submit_button = driver.find_element_by_id('neugruendungen_searchbutton')
submit_button.click()
print('Finally done with the preparation')

loadmorebutton=driver.find_element_by_class_name('show-more-news-link')					#clicks the "show more" button to load more companies
i=10
while loadmorebutton.size!=0:										#this is a mess. It clicks the "show more button"
	try:												#and tells you about it with a print command.
		loadmorebutton.click()									#once it can't click anymore, it breaks out of the loop
		WebDriverWait(driver, 5)
	except:
		break
	finally:
		print('loaded')
		print(i)
		i=i+10
		print('more data sets')
		print('')

print('Starting to scrap!')											
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'link-list__link')))	#we wait a bit and then start scraping
print('')
print('Results are being loaded. Please wait.')
company_name=driver.find_elements_by_class_name('link-list__link')					#here we get all the data which you can find in the readme.md and prints it
company_description=driver.find_elements_by_class_name('link-list__desc')
wko_link=driver.find_elements_by_class_name('link-list__link')
for x in range(len(company_name)):
	print(company_name[x].text)
	print(company_description[x].text)
	print("WKO Link: " + wko_link[x].get_attribute('href'))
	print('')

print('Writing data in csv')										#a print command so you know that the program is working. it just takes a while

with open('newCompanies.csv', 'w', newline='') as file:							#the data is being written in a csv file.
	company_name=driver.find_elements_by_class_name('link-list__link')
	company_description=driver.find_elements_by_class_name('link-list__desc')
	wko_link=driver.find_elements_by_class_name('link-list__link')
	writer = csv.writer(file)
	for x in range(len(company_name)):
		writer.writerow([company_name[x].text])
		writer.writerow([company_description[x].text])
		writer.writerow(["WKO Link: ", wko_link[x].get_attribute('href')])
		writer.writerow([])
	driver.quit()
