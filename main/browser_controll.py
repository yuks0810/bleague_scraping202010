from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

class BrowserControll:

    def __init__(self, driver, league, season, event, club, setuFrom):
        super().__init__()
        print("start CrowserControll class")
        self.driver = driver
        self.league = league
        self.season = season
        self.event = event
        self.club = club
        self.setuFrom = setuFrom


    def select_B1_B2(self):
        b1 = self.driver.find_element_by_xpath('//input[@id="tab1" and @name="tab" and @type="radio"]')
        b2 = self.driver.find_element_by_xpath('//input[@id="tab2" and @name="tab" and @type="radio"]')

        print("B", self.league, "を選択します")
        if target == "B1":
            b1.click()
        else:
            b2.click()

    def select_report(self, date=datetime.datetime.now()):
        # レポートタグをクリックしてスクレイピングしたい対象のでテーブルをタブで開く
        a_tags = self.driver.find_elements_by_xpath('//a[@rel="noopener" and @class="btn btn-rd"]') 
        href_arry = []

        for a_tag in a_tags:
            # print(a_tag.get_attribute("href"))
            href_arry.append(a_tag.get_attribute("href"))

        href_count = len(href_arry)

        for i, url in enumerate(href_arry):
            self.driver.execute_script("window.open()") #make new tab
            self.driver.switch_to.window(self.driver.window_handles[i+1]) #switch new tab
            self.driver.get(url)
            if i > 2:
                break

    def create_report_href_arry(self):
        a_tags = self.driver.find_elements_by_xpath('//a[@rel="noopener" and @class="btn btn-rd"]') 
        href_arry = []

        for a_tag in a_tags:
            # print(a_tag.get_attribute("href"))
            href_arry.append(a_tag.get_attribute("href"))

        href_count = len(href_arry)

        return href_arry, href_count