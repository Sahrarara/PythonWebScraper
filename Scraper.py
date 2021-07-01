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
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cookieagree")))
cookie_button = driver.find_element_by_class_name('cookieagree').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-success')))
location = driver.find_element_by_xpath('//input[@value="w"]')
search = WebDriverWait(driver, 3)
location.click()
print('dang popup windows, I swear')
WebDriverWait(driver,3)
search_form = driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[3]/button').click()
submit_button = driver.find_element_by_id('neugruendungen_searchbutton')
submit_button.click()
print('so many popups...')

loadmorebutton=driver.find_element_by_class_name('show-more-news-link')
i=10
while loadmorebutton.size!=0:
	try:
		loadmorebutton.click()
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
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'link-list__link')))
loadmorebutton=driver.find_element_by_class_name('show-more-news-link')
print('')
print('Results are being loaded. Please wait.')
company_name=driver.find_elements_by_class_name('link-list__link')
company_description=driver.find_elements_by_class_name('link-list__desc')
wko_link=driver.find_elements_by_class_name('link-list__link')
for x in range(len(company_name)):
	print(company_name[x].text)
	print(company_description[x].text)
	print("WKO Link: " + wko_link[x].get_attribute('href'))
	print('')

print('Writing data in csv')

with open('newCompanies.csv', 'w', newline='') as file:
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
