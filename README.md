# bleague_scraping202010
B league scraping with python, after the website update. 

## 使い方
### cloneしてくる
Desktopなど使う場所にファイルをダウンロードする
`git clone https://github.com/yuks0810/bleague_scraping202010.git`

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
