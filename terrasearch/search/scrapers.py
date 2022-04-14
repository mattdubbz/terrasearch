from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))


# scrape for-sale properties
def scrape_for_sale(url):
    pass


# scrape sold properties
def scrape_sold(url):
    pass
