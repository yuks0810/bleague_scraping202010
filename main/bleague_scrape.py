import time
import sys
# import classes
from browser_controll import BrowserControll
# selenium chrome driverの最新verをインストール
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # オプションを使うために必要

# g_spread
from g_spread_sheet.game_report_g_spread import GameReportGSpread

def set_params(inputs):
    league = inputs[0]
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
print("シートを削除したい場合は delete と入力してください。")
inputs = input().split(",")

if not len(inputs) == 5:
    if not inputs[0] == "delete":
        print("有効な値を入力してください")
        sys.exit()

if not inputs[0] == "delete":
    second_input = inputs[1].split("-")
    if not len(second_input[0]) == 4 or not len(second_input[1]) == 2:
        print("有効な値を入力してください（シーズン）")
        print("シーズンの項目は2019-19のようにハイフンで区切り、4桁と2桁の数字を使ってください")
        sys.exit()

if inputs[0].lower() == "delete":
    game_report_for_delete = GameReportGSpread(delete=True)
    workbook = game_report_for_delete.connect_workbook()
    game_report_for_delete.delete_all_sheets(workbook)
    sys.exit()


print('updating chrome driver start')
option = Options()                          # オプションを用意
option.add_argument('--headless')           # ヘッドレスモードの設定を付与 

# ヘッドレスで実行するとき
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
# ブラウザを表示するとき
# driver = webdriver.Chrome(ChromeDriverManager().install())
print('updating chrome driver end')



league, season, event, club, setuFrom = set_params(inputs)

# Webページへアクセス
driver.get('https://www.bleague.jp/schedule/?s=1&tab={tab}&year=2018&event={event}&club=&setuFrom={setuFrom}'.format(tab=league, year=league, event=event, setuFrom=setuFrom))
driver.implicitly_wait(15)
# print('https://www.bleague.jp/schedule/?s=1&tab={tab}&year=2018&event={event}&club=&setuFrom={setuFrom}'.format(tab=league, year=league, event=event, setuFrom=setuFrom))
# time.sleep(3)

brows = BrowserControll(driver, league, season, event, club, setuFrom)
# brows.select_report()
href_arry, href_count = brows.create_report_href_arry()

for i, url in enumerate(href_arry):
    driver.execute_script("window.open()") # make a new tab
    driver.switch_to.window(driver.window_handles[i+1]) #switch new tab
    driver.get(url)
    
    game_report = GameReportGSpread(driver)
    game_report.get_game_teams()
    game_report.get_year()
    game_report.get_date_time()
    game_report.write_table()

print('処理が正常に終了しました')

# # テーブル内容取得
# tableElem = driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[1]/table')
# # trs = tableElem.find_elements(By.TAG_NAME, "tr")
    
# tds = tableElem.find_elements_by_tag_name('td')
# for td in tds:
#     # import pdb; pdb.set_trace()
#     print(td.get_attribute("textContent"))


