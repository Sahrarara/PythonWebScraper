from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re


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
print('Preparation done. Loading data sets')


loadmorebutton=driver.find_element_by_class_name('show-more-news-link')					#clicks the "show more" button to load more companies
i=10
while loadmorebutton.size!=0:										#this is a mess. It clicks the "show more button"
	try:												#and tells you about it with a print command.
		loadmorebutton.click()									#once it can't click anymore, it breaks out of the loop
		WebDriverWait(driver, 5)
	except:
		break
	finally:
		print('loaded ' , i , 'more data sets')
		i=i+10
		print('')

print('Starting to scrap!')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'link-list__link')))	#we wait a bit and then start scraping
print('')

namelist=[]
desclist=[]
addrlist=[]
linklist=[]
i=1
print('Results are being loaded. Please wait.')
company_name=driver.find_elements_by_class_name('link-list__link')					#here we get most data. Only the address is hidden behind the href link
company_description=driver.find_elements_by_class_name('link-list__desc')
wko_link=driver.find_elements_by_class_name('link-list__link')
for x in range(len(company_name)):
	namelist.append(company_name[x].text)
	desclist.append(company_description[x].text)
	linklist.append(wko_link[x].get_attribute('href'))
	print('Appending to lists.', i , 'appended items')
	i=i+1
print('appended all' , i-1 , 'items. Starting next task')

j=1
try:
	for x in range(len(linklist)):									#uses the links in the linklist to open the site and scrape the address from there.
		if linklist[x]!='https://www.wko.at/service/neuzugaenge.html#':
			driver.get(linklist[x])
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.row:nth-child(2) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)')))
			addr=driver.find_element_by_css_selector('div.row:nth-child(2) > div:nth-child(1) > p:nth-child(2) > span:nth-child(2)').text
			addrlist.append(re.sub("\(kann vom Gründungsdatum abweichen\)", "", addr))
			print('got address nr.' , j)							#printing the number so you can easier find it in the csv file
			j=j+1
		else:
			addrlist.append('bad link, thus no data')					#sometimes there is a link to the wko site itself. that's considered a bad link
			print('bad link')
			j=j+1
except:
	print('an error has occured')

print('Writing data in csv')										#a print command so you know that the program is working. it just takes a while
j=1
with open('newCompanies.csv', 'w', newline='') as file:							#the data is being written in a csv file.
	writer = csv.writer(file)
	writer.writerow(['', 'Firmenname', 'Adresse', 'Beschreibung', 'WKO-Link'])
	for x in range(len(namelist)):
		writer.writerow([j, namelist[x], addrlist[x], desclist[x], linklist[x]])
		print(j, ' of ' ,i-1, ' items have been written in the csv')
		j=j+1
	driver.quit()
print('Data has been succesfully scraped')
