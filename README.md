# bleague_scraping202010
B league scraping with python, after the website update. 

対象ページ：
https://www.bleague.jp/game_detail/?ScheduleKey=5934

対象ページの「GAME REPORT」、「PLAY BY PLAY」、「BOX SCORE」タブにあるテーブルを検索条件などに応じてgoogle spread sheetに書き込みを行う。

## 使用API
### gspread: Google Spread Sheet操作API
https://gspread.readthedocs.io/en/latest/

### selenium（WebDriver API）: ブラウザ操作ライブラリ
https://kurozumi.github.io/selenium-python/api.html

## 使い方
### cloneしてくる
Desktopなど使う場所にファイルをダウンロードする
`git clone https://github.com/yuks0810/bleague_scraping202010.git`

### 必要パッケージをインストール
terminalで

```bash
$ pip install webdriver-manager
```
最新版はこのサイトを確認：
https://pypi.org/project/webdriver-manager/

### Anaconda 仮想環境準備
Anacondaなどでパッケージを使える環境を整える
`./Bleague_scraping202010.yml`
ファイルをもとにconda環境を再構築する

ex)

```bash
$ conda env create -n Bleague_scraping202010 -f Bleague_scraping202010.yml
```

Anacondaの仮想環境をactivateする

```bash
$ conda activate Bleague_scraping202010
```

### 実行
対象フォルダルートまで移動して下記コマンドでファイルを実行する

```bash
$ python main/bleague_scrape.py
```

下記のように聞かれるので、検索したい項目を入力する

```
リーグ, シーズン, 大会, クラブ, 節 の準で入力してください。ex) B2,2018-19,7,7,2 
大会を数字で入力してください。ex) 7:B2リーグ, 5:オールスターゲーム, 9:B2残留プレーオフ, 8:B2プレーオフ, 11:B1・B2入替戦, 17:B2・B3入替戦, 20:アーリーカップ
```
ex) 

```bash
$ リーグ, シーズン, 大会, クラブ, 節 の準で入力してください。ex) B2,2018-19,7,7,2 
大会を数字で入力してください。ex) 7:B2リーグ, 5:オールスターゲーム, 9:B2残留プレーオフ, 8:B2プレーオフ, 11:B1・B2入替戦, 17:B2・B3入替戦, 20:アーリーカップ

B2,2018-19,7,7,2
```
## 対象のgoogle spread sheetを変更する際のキーの見方
![スクリーンショット 2020-10-25 17 51 33](https://user-images.githubusercontent.com/49354810/97122983-d4430180-176c-11eb-95fd-1451cdaf683e.png)

## google spread sheet
test spread sheet:
https://docs.google.com/spreadsheets/d/1Jrj9EoSqUcD9L3q0JoDobzc-KO25lon9Aq_rV98EkPA/edit#gid=0

### 秘密鍵
bleague_scraping_g_spread_key.dmgというファイルに秘密情報が載っている

