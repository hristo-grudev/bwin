import datetime
import time

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ..items import BwinItem


class ProductSpider(scrapy.Spider):
    name = "bwin"
    start_urls = [r'https://sports.bwin.com/bg/sports/%D1%84%D1%83%D1%82%D0%B1%D0%BE%D0%BB-4/%D1%83%D1%82%D1%80%D0%B5']

    def __init__(self):
        PATH = 'C:\Program Files\chromedriver.exe'
        self.driver = webdriver.Chrome(PATH)

    def string_to_date(self, string_date):
        string = string_date.split('/')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        date = datetime.datetime.strptime(str(tomorrow) + string[1], '%Y-%m-%d %H:%M')
        return date

    def parse(self, response):
        delay = 10  # seconds
        self.driver.get(response.url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        table = self.driver.find_element_by_xpath('//ms-grid')

        for row in table.find_elements_by_xpath('.//div[@class="grid-event-wrapper"]'):
            participants = row.find_elements_by_xpath('.//div[@class="participant"]')
            coefficients = row.find_elements_by_xpath('.//div[@class="option-indicator"]')
            date = row.find_elements_by_xpath('.//*[contains(@class,"starting-time")]')
            try:
                site = 'bwin'
                sport = 'football'
                participant1 = participants[0].text
                participant2 = participants[1].text
                coeff1 = coefficients[0].text
                coeffX = coefficients[1].text
                coeff2 = coefficients[2].text
                date = self.string_to_date(date[0].text)
                print(participant1, participant2, coeff1, coeffX, coeff2, date)

                item = ItemLoader(item=BwinItem(), response=response)
                item.default_output_processor = TakeFirst()
                item.add_value('site', site)
                item.add_value('sport', sport)
                item.add_value('date', date)
                item.add_value('participant1', participant1)
                item.add_value('participant2', participant2)
                item.add_value('coeff1', coeff1)
                item.add_value('coeffX', coeffX)
                item.add_value('coeff2', coeff2)
                yield item.load_item()

            except Exception as e:
                print(e)
                pass

        # participants = table.find_element_by_class_name('participants-pair-game')
        # time = table.find_element_by_class_name('grid-event-info')
        # print(participants.text)
        # print(time.text)
