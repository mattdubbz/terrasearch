from celery import shared_task

from .scrapers import scrape_for_sale, scrape_sold

FOR_SALE_URL = "https://www.realtor.com/"
SOLD_URL = "https://www.realtor.com/soldhomes"


@shared_task
def scrape_async():
    scrape_for_sale(FOR_SALE_URL)
    scrape_sold(SOLD_URL)
    return
