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
from g_spread_sheet.box_score_g_spread import BoxScoreGSpread
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

def get_box_score():
    brows = BrowserControll(driver, league, season, event, club, setuFrom)

    # brows.select_report()
    href_arry, href_count = brows.create_box_score_href_arry()

    for i, url in enumerate(href_arry):
        driver.execute_script("window.open()") # make a new tab
        driver.switch_to.window(driver.window_handles[i+1]) #switch new tab
        driver.get(url)
        
        box_score = BoxScoreGSpread(driver)
        box_score.get_game_teams()
        box_score.get_year()
        box_score.get_date_time()
        box_score.get_game_url()
        box_score.write_table()

def get_game_report():
    brows = BrowserControll(driver, league, season, event, club, setuFrom)

    href_arry, href_count = brows.create_box_score_href_arry()

    for i, url in enumerate(href_arry):        
        driver.execute_script("window.open()") # make a new tab
        driver.switch_to.window(driver.window_handles[i+1]) #switch new tab
        driver.get(url)

        game_report = GameReportGSpread(driver, url)
        game_report.get_game_teams()
        game_report.get_year()
        game_report.get_date_time()
        game_report.write_table()
        # game_report.get_game_url()

        time.sleep(5)

# リセット処理
def reset_game_report_g_spread_sheets():
    game_report_for_delete = GameReportGSpread(delete=True)
    workbook = game_report_for_delete.connect_workbook()
    game_report_for_delete.delete_all_sheets(workbook)
    print('GAME REPORT リセット完了')

def reset_box_score_g_spread_sheets():
    box_score_for_delete = BoxScoreGSpread(delete=True)
    workbook = box_score_for_delete.connect_workbook()
    box_score_for_delete.delete_all_sheets(workbook)
    print('BOX SCORE リセット完了')
    
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

# 削除する時の動作、削除が終わったらプログラムを終了する。
if inputs[0].lower() == "delete":
    print("リセットしたいスプレッドシートを選択してください。※数字で入力してください。【GAME REPORT: 1, PLAY BY PLAY: 2, BOX SCORE: 3】")
    print("複数選択する場合は 1,2,3 のようにカンマ区切りで入力してください。")
    chose_reset_sheet_type = input().split(",")

    if "1" in chose_reset_sheet_type:
        reset_game_report_g_spread_sheets()
    if "2" in chose_reset_sheet_type:
        reset_play_by_play_g_spread_sheets()
    if "3" in chose_reset_sheet_type:
        reset_box_score_g_spread_sheets()
    sys.exit()


print("取得したい項目を入力してください。※数字で入力してください。【GAME REPORT: 1, PLAY BY PLAY: 2, BOX SCORE: 3】")
print("複数選択する場合は 1,2,3 のようにカンマ区切りで入力してください。")
input_to_chose_type = input().split((','))

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


if '1' in input_to_chose_type:
    get_game_report()

# if '2' in input_to_chose_type:
#     get_play_by_play()

if '3' in input_to_chose_type:
    get_box_score()



print('処理が正常に終了しました')
