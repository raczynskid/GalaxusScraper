from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import dataclass

@dataclass
class Transaction:
    timestamp: str
    event_type: str
    product: str
    url: str

driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver = webdriver.Chrome(options=options)
target_url = 'https://www.galaxus.ch/en/daily-deal'
driver.get(target_url)


all_events = []
for transaction in driver.find_elements(By.XPATH, "//aside/section/div/div/div/div/div")[:4]:
    timestamp = transaction.find_element(By.XPATH, "div[1]/span[@type]").text
    event_type = transaction.find_element(By.XPATH, "div/span[@type]").get_attribute('type')

    try:
        product_name = str.strip(transaction.find_element(By.XPATH, "a").get_attribute('aria-label'))
        url = transaction.find_element(By.XPATH, "a").get_attribute('href')
    except:
        product_name = ""
        url = ""
    
    event_instance = Transaction(timestamp=timestamp, event_type=event_type, product=product_name, url=url)
    all_events.append(event_instance)
all_events

