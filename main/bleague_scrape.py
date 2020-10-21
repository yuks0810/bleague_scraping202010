import time
# import classes
from browser_controll import BrowserControll
# selenium chrome driverの最新verをインストール
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def set_params(inputs):
    league =         inputs[0]
    if league == "B1":
        league = 1
    else:
        league = 2

    season =         inputs[1]
    event =          inputs[2]
    club =           inputs[3]
    setuFrom =       inputs[4]
    return league, season, event, club, setuFrom


print("リーグ, シーズン, 大会, クラブ, 節 の準で入力してください。ex) B2,2018-19,7,7,2 \n大会を数字で入力してください。ex) 7:B2リーグ, 5:オールスターゲーム, 9:B2残留プレーオフ, 8:B2プレーオフ, 11:B1・B2入替戦, 17:B2・B3入替戦, 20:アーリーカップ")
inputs = input().split(",")
league, season, event, club, setuFrom = set_params(inputs)



print('updating chrome driver start')
driver = webdriver.Chrome(ChromeDriverManager().install())
print('updating chrome driver end')

driver.get('https://www.bleague.jp/schedule/?s=1&tab={tab}&year=2018&event={event}&club=&setuFrom={setuFrom}'.format(tab=league, year=league, event=event, setuFrom=setuFrom))
# print('https://www.bleague.jp/schedule/?s=1&tab={tab}&year=2018&event={event}&club=&setuFrom={setuFrom}'.format(tab=league, year=league, event=event, setuFrom=setuFrom))
# time.sleep(3)

brows = BrowserControll(driver, league, season, event, club, setuFrom)


