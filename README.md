# PythonWebScraper

During my traineeship I made a webscraper for the wko website.
I was tasked with scraping data from newly founded companies.
Things scraped:
* Name of the company
* Address of the company
* Short description of the kind of company they are (Sales, Marketing, etc)
* WKO link for more information

It is a bit over the top, since the script gives out a lot of print commands so you know it's working before writing it in a csv file. 
Also, it only uses firefox via the geckodriver. Chrome, etc isn't supported.
I also don't know if it works in windows. It should, but I haven't tried it.
Made with python 3.7.3


## Important!
Download Geckodriver! 
Don't forget to set the PATH to the geckodriver before running the scraper! Selenium is weird like that.
