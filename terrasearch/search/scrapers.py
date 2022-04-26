from django.shortcuts import get_object_or_404
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

from .models import ForSaleProperty, Search, SoldProperty

# create the driver with the propert options
opts = Options()
opts.add_argument("--headless")
# opts.set
driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()), options=opts
)


# scrape for-sale properties
def scrape_for_sale(url, search_pk):

    try:
        WebDriverWait(driver, timeout=10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='rui__ermeke-1 YoPbk rui__p9wrku-1 ugMaj']")
            )
        )
        # ".//li[@class='jsx-1881802087 component_property-card']"

        # intitial search
        driver.find_element(By.XPATH, '//*[@id="searchbox-input"]').send_keys(
            "Forney, TX"
        )
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div/div/div/form/div/button",
        ).click()

        # wait until <ul> property-list list-unstyle is loaded
        WebDriverWait(driver, timeout=10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[3]/section/ul")
            )
        )

    except TimeoutException:
        print("Timed out waiting on page to load")
        driver.quit()

    try:

        # get each <li> property-list list-unstyle
        list_elements = driver.find_elements(
            By.XPATH, ".//li[@class='jsx-1881802087 component_property-card']"
        )
        # print(list_elements)

        for element in list_elements:
            # print(element.text)
            WebDriverWait(driver, timeout=10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, ".//div[@class='jsx-1489967104 card-bottom']")
                )
            )

            # get link to prop
            a_tag = element.find_element(
                By.XPATH, ".//a[@class='jsx-1534613990 card-anchor']"
            )
            link = a_tag.get_attribute("href")
            # print(link)

            # get image from <img> fade top
            img = a_tag.find_element(By.XPATH, ".//img[last()]").get_attribute("src")
            # print(img)

            # get lead_prop description here
            prop_descr = element.text
            # print(lead_descr)
            # get list price
            list_price_str = element.find_element(
                By.XPATH,
                ".//div[@class='jsx-1489967104 ldp-redesign-price srp-page-price']",
            ).text[1:]
            list_price = int(list_price_str.replace(",", ""))
            # print(list_price)

            # get list of beds, baths, sqft
            bbs_list = element.find_elements(
                By.XPATH, ".//li[@class='jsx-946479843 prop-meta srp_list']"
            )

            bed_li = bbs_list[0]
            bed_num_str = bed_li.find_element(
                By.XPATH, ".//span[@data-label='meta-value']"
            ).text
            bed_num = int(bed_num_str)
            # print(bed_num)

            bath_li = bbs_list[1]
            bath_num_str = bath_li.find_element(
                By.XPATH, ".//span[@data-label='meta-value']"
            ).text
            bath_num = float(bath_num_str)
            # print(bath_num)

            sqft_li = bbs_list[2]
            sqft_str = sqft_li.find_element(
                By.XPATH, ".//span[@data-label='meta-value']"
            ).text
            sqft = int(sqft_str.replace(",", ""))
            # print(sqft)

            # OPTIONAL get sqft of the lot, currently not needed
            # lot_sqft_li = bbs_list[3]
            # lot_sqft_str = lot_sqft_li.find_element(
            #     By.XPATH, ".//span[@data-label='meta-value']").text
            # lot_sqft = int(sqft_str.replace(",", ""))
            # print(lot_sqft)

            full_address = element.find_element(
                By.XPATH,
                ".//div[@class='jsx-1489967104 address ellipsis srp-page-address srp-address-redesign']",
            ).text
            # print(full_address)
            a_list = full_address.split(",")
            address = a_list[0]
            # print(address)
            city = a_list[1].strip()
            # print(city)
            st_zip_list = a_list[2]
            st_zip_list = st_zip_list.strip()
            st_zip_list = st_zip_list.split(" ")
            state = st_zip_list[0]
            # print(state)
            zip = st_zip_list[1]
            # print(zip)

            # get the current Search object
            search = get_object_or_404(Search, pk=search_pk)

            # create ForSale object
            ForSaleProperty.objects.create(
                search=search,
                list_price=list_price,
                image=img,
                link=link,
                description=prop_descr,
                beds=bed_num,
                baths=bath_num,
                sqft=sqft,
                address=address,
                city=city,
                state=state,
                zip=zip,
            )

    except ValueError:
        pass
    except IndexError:
        pass
    except Exception as e:
        print(e)


# scrape sold properties
def scrape_sold(url, search_pk):

    try:

        driver.find_element(By.XPATH, '//*[@id="searchbox-input"]').send_keys(
            "Tampa, FL"
        )
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div/div/div/form/div/button",
        ).click()

        # wait until <ul> property-list list-unstyle is loaded
        WebDriverWait(driver, timeout=10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[3]/section/ul")
            )
        )

    except TimeoutException:
        print("Timed out waiting on page to load")
        driver.quit()

    try:
        # get each <li> property-list list-unstyle
        list_elements = driver.find_elements(
            By.XPATH, ".//li[@class='jsx-1881802087 component_property-card']"
        )
        # print(list_elements)

        for element in list_elements:
            # print(element.text)
            WebDriverWait(driver, timeout=10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, ".//div[@class='jsx-1489967104 card-bottom']")
                )
            )

            # get link to prop
            a_tag = element.find_element(
                By.XPATH, ".//a[@class='jsx-1534613990 card-anchor']"
            )
            link = a_tag.get_attribute("href")
            print(link)

            # get image from <img> fade top
            img = a_tag.find_element(By.XPATH, ".//img[last()]").get_attribute("src")
            # print(img)

            # get lead_prop description here
            prop_descr = element.text
            # print(lead_descr)
            # get list price
            sold_price_str = element.find_element(
                By.XPATH,
                ".//div[@class='jsx-1489967104 ldp-redesign-price srp-page-price']",
            ).text[1:]
            sold_price = int(sold_price_str.replace(",", ""))
            # print(sold_price)

            # get list of beds, baths, sqft
            bbs_list = element.find_elements(
                By.XPATH, ".//li[@class='jsx-946479843 prop-meta srp_list']"
            )

            bed_li = bbs_list[0]
            bed_num_str = bed_li.find_element(
                By.XPATH, ".//span[@data-label='meta-value']"
            ).text
            bed_num = int(bed_num_str)
            # print(bed_num)

            bath_li = bbs_list[1]
            bath_num_str = bath_li.find_element(
                By.XPATH, ".//span[@data-label='meta-value']"
            ).text
            bath_num = float(bath_num_str)
            # print(bath_num)

            sqft_li = bbs_list[2]
            sqft_str = sqft_li.find_element(
                By.XPATH, ".//span[@data-label='meta-value']"
            ).text
            sqft = int(sqft_str.replace(",", ""))
            # print(sqft)

            # lot_sqft_li = bbs_list[3]
            # lot_sqft_str = lot_sqft_li.find_element(
            #     By.XPATH, ".//span[@data-label='meta-value']").text
            # lot_sqft = int(sqft_str.replace(",", ""))
            # print(lot_sqft)

            full_address = element.find_element(
                By.XPATH,
                ".//div[@class='jsx-1489967104 address ellipsis srp-page-address srp-address-redesign']",
            ).text
            # print(full_address)
            a_list = full_address.split(",")
            address = a_list[0]
            # print(address)
            city = a_list[1].strip()
            # print(city)
            st_zip_list = a_list[2]
            st_zip_list = st_zip_list.strip()
            st_zip_list = st_zip_list.split(" ")
            state = st_zip_list[0]
            # print(state)
            zip = st_zip_list[1]
            # print(zip)

            # get the current Search object
            search = get_object_or_404(Search, pk=search_pk)

            # create SoldProperty object
            SoldProperty.objects.create(
                search=search,
                sold_price=sold_price,
                image=img,
                link=link,
                description=prop_descr,
                beds=bed_num,
                baths=bath_num,
                sqft=sqft,
                address=address,
                city=city,
                state=state,
                zip=zip,
            )

    except ValueError:
        pass
    except IndexError:
        pass
    except Exception as e:
        print(e)
