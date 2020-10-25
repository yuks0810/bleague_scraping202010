import time
# import classes
from browser_controll import BrowserControll
# selenium chrome driverの最新verをインストール
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# g_spread
from g_spread_sheet.game_report_g_spread import GameReportGSpread

def set_params(inputs):
    league =         inputs[0]
    if league == "B1":
        league = 1
    else:
        league = 2

    season   = inputs[1]
    event    = inputs[2]
    club     = inputs[3]
    setuFrom = inputs[4]
    return league, season, event, club, setuFrom


print("リーグ, シーズン, 大会, クラブ, 節 の準で入力してください。ex) B2,2018-19,7,7,2 \n大会を数字で入力してください。ex) 7:B2リーグ, 5:オールスターゲーム, 9:B2残留プレーオフ, 8:B2プレーオフ, 11:B1・B2入替戦, 17:B2・B3入替戦, 20:アーリーカップ")
inputs = input().split(",")
league, season, event, club, setuFrom = set_params(inputs)


print('updating chrome driver start')
driver = webdriver.Chrome(ChromeDriverManager().install())
print('updating chrome driver end')

# Webページへアクセス
driver.get('https://www.bleague.jp/schedule/?s=1&tab={tab}&year=2018&event={event}&club=&setuFrom={setuFrom}'.format(tab=league, year=league, event=event, setuFrom=setuFrom))
driver.implicitly_wait(15)
# print('https://www.bleague.jp/schedule/?s=1&tab={tab}&year=2018&event={event}&club=&setuFrom={setuFrom}'.format(tab=league, year=league, event=event, setuFrom=setuFrom))
# time.sleep(3)

brows = BrowserControll(driver, league, season, event, club, setuFrom)
brows.select_report()

game_report = GameReportGSpread(driver)
game_report.get_game_teams()
game_report.get_year()
game_report.get_date_time()
game_report.write_thead()

# # テーブル内容取得
# tableElem = driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[1]/table')
# # trs = tableElem.find_elements(By.TAG_NAME, "tr")
    
# tds = tableElem.find_elements_by_tag_name('td')
# for td in tds:
#     # import pdb; pdb.set_trace()
#     print(td.get_attribute("textContent"))


