import time
import random
import os
import pandas as pd
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class GoogleMapsScraper:

    def __init__(self, niche, city, quantity):
        self.niche = niche
        self.city = city
        self.quantity = quantity
        self.data = []

        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 15)

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _delay(self, min_time=1.5, max_time=3.5):
        time.sleep(random.uniform(min_time, max_time))

    def _scroll_results(self):
                scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

                for _ in range(10):
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",scrollable_div)
                    self._delay(1, 2)

    def search(self):
        search_query = f"{self.niche}, {self.city}"
        encoded_query = quote (search_query)
        url = f"https://www.google.com/maps/search/{encoded_query}"

        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nv2PK')))

        self._scroll_results()
        self._delay(2, 4)

    def _get_filtered_cards(self):
        cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')
        filtered = []

        for card in cards:
             try:
                card.find_element(By.XPATH,".//*[contains(text(), 'Sponsored') or contains(text(), 'Patrocinado')]")
                continue
             except:
                  filtered.append(card)
        return filtered 
    
    def excract(self):
         for i in range(self.quantity):
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nv2PK')))
            companies = self._get_filtered_cards()

            if i >= len(companies):
                break

            company = companies[i]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", company)

            self._delay(1, 2)
            company.click()

            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf')))

            self._delay()

            name = self.driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text

            try:
                phone_raw = self.driver.find_element(By.CSS_SELECTOR,'button[data-item-id^="phone"]').text
                phone = phone_raw.split("\n")[-1]
            except:
                phone = "Not available"

            try:
                website = self.driver.find_element(By.CSS_SELECTOR,'a[data-item-id="authority"]').get_attribute("href")
            except:
                website = "Not available"

            try:
                address = self.driver.find_element(By.CSS_SELECTOR,'button[data-item-id="address"]').text.replace("\n", ", ")
            except:
                address = "Not available"

            self.data.append({
                "name": name,
                "phone": phone,
                "website": website,
                "address": address
            })

            print(f"{i+1} - {name}")

            back_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[aria-label*="Back"], button[aria-label*="Voltar"]')))
            back_button.click()

            self._delay(1.5, 3)

    def save_to_csv(self):
        df = pd.DataFrame(slf.data, columns=["name", "phone", "website", "address"])
        
        file_path = os.path.join(os.getcwd(), "leads.csv")

        df.to_csv(file_path, index=False, sep=";", encoding="utf-8-sig")

        print("File saved successfully")

    def run(self):
        self.search()
        self.excract()
        self.save_to_csv()
        self.driver.quit()