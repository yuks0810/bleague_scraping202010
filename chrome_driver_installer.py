from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.bleague.jp/schedule/?tab=1&year=2020&event=2')