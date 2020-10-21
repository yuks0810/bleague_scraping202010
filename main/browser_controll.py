from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

class BrowserControll:

    def __init__(self, driver, league, season, event, club, setuFrom):
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
