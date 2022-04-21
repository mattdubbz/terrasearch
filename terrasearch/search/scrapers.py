from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


# scrape for-sale properties
def scrape_for_sale(url):
    # create the driver with the propert options
    opts = Options()
    opts.set_headless()
    assert opts.headless  # Operating in headless mode
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()), options=opts
    )


# scrape sold properties
def scrape_sold(url):
    # create the driver with the propert options
    opts = Options()
    opts.set_headless()
    assert opts.headless  # Operating in headless mode
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()), options=opts
    )
