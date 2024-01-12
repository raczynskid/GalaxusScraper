#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dataclasses import dataclass



@dataclass
class Transaction:
    timestamp: str
    event_type: str
    product: str
    supplier: str = None
    price: float = None
    location: str = None
    url: str = None
    description: str = None

    def format_as_tuple(self):
        return(self.timestamp, self.event_type, self.product, self.supplier, self.price, self.location, self.url, self.description)

def set_webdriver():
    options = webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)
    return driver

target_url = 'https://www.galaxus.ch/en/daily-deal'
driver = set_webdriver()

def extract_location(description: str) -> str:
    return description.split(" from ")[-1].split(" ")[0].capitalize()

def get_feed():
    all_events = []
    driver.implicitly_wait(3)
    driver.execute_script("window.scrollBy(5000,40)")
    for transaction in driver.find_elements(By.XPATH, "//aside/section/div/div/div/div/div")[:4]:
        timestamp = transaction.find_element(By.XPATH, "div[1]/span[@type]").text
        event_type = transaction.find_element(By.XPATH, "div/span[@type]").get_attribute('type')

        try:
            product_name = str.strip(transaction.find_element(By.XPATH, "a").get_attribute('aria-label'))
            url = transaction.find_element(By.XPATH, "a").get_attribute('href')
            if event_type == 'product':
                supplier = transaction.find_element(By.XPATH, "div//span[not (@type)]/strong").text
                price = transaction.find_element(By.XPATH, "div//strong[@class]/span").text
            else:
                supplier = None
                price = None

        except NoSuchElementException:
            product_name = None
            url = None
            supplier = None
            price = None

        description: str = transaction.find_element(By.XPATH, "div//span[not (@type)]").text
        location: str  = extract_location(description)
        
        if timestamp:
            event_instance = Transaction(timestamp = timestamp, event_type = event_type, product = product_name, supplier = supplier, price = price, location = location, url = url, description=description)
            all_events.append(event_instance)
            price = None
    return all_events

result = get_feed()
result

# TODO move to RPi