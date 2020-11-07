import time
class GameReportGSpread:

    def __init__(self, driver=None, delete=False):
        super().__init__()
        import json

        # ここでjsonfile名と2-2で用意したkeyを入力
        self.driver = driver
        self.jsonf = "dynamic-density-293202-cfdad7f5ab26.json"
        self.spread_sheet_key = "1HjPQNCtO6WWCsrFEOCehemHwqj2C-35IbX-wZBPMbGc"

        if delete == False:
            self.ws = self.__connect_gspread(self.jsonf, self.spread_sheet_key)
        
            # カラムの数が40個なければ作成する
            col_num = self.ws.col_count
            self.ws.add_cols(40 - col_num)

    def get_game_teams(self):
        venue_name = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[3]/p[1]')
        self.ws.update_acell('A1', venue_name.get_attribute("textContent"))

    def get_year(self):
        year = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[1]')
        self.ws.update_acell('A2', year.get_attribute("textContent"))

    def get_date_time(self):
        month = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[2]/span')
        week = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[3]/span[1]')
        time = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[4]')

        cell_list = self.ws.range('A3:C3')
        m_w_t = [
            month.get_attribute("textContent"), 
            week.get_attribute("textContent"),
            time.get_attribute("textContent")
            ]

        for i, cell in enumerate(cell_list):
            val =  m_w_t[i]
            cell.value = val

        self.ws.update_cells(cell_list, value_input_option='USER_ENTERED')
    
    def write_table(self):
        # theads = []
        # theads.append(self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[1]/table/thead'))
        # theads.append(self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[2]/table/thead'))
        theads = self.driver.find_elements_by_tag_name('thead')
        tbodies = self.driver.find_elements_by_tag_name('tbody')

        # tbodiesだけ余計なtableがあるのでBOX SCOREのみを抽出するために削除
        del tbodies[0:3]

        for idx, thead in enumerate(theads):
            if idx == 0:
                cell_list = self.ws.range(6, 1, 6, 27)
                thead_row = 6
            else:
                cell_list = self.ws.range(idx * 24, 1, idx * 24, 27)
                thead_row = idx * 24

            ths = thead.find_element_by_tag_name('tr').find_elements_by_tag_name('th')
            for i, cell in enumerate(cell_list):
                val = ths[i].get_attribute("textContent")
                cell.value = val
                
            self.ws.update_cells(cell_list, value_input_option='USER_ENTERED')
            self.__write_tbody_contents(tbodies[idx], thead_row)
            time.sleep(10)

    def delete_all_sheets(self, workbook):
        idx = 0
        for ws in workbook.worksheets():
            idx += 1
            if idx > 1:
                workbook.del_worksheet(ws)

    def connect_workbook(self):
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials

        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.jsonf, scope)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = self.spread_sheet_key
        workbook = gc.open_by_key(SPREADSHEET_KEY)
        return workbook

    ## private 

    def __connect_gspread(self, jsonf, key):
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials

        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = key
        workbook = gc.open_by_key(SPREADSHEET_KEY)

        year = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[1]').get_attribute('textContent')
        month = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[2]/span').get_attribute('textContent')
        week = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[3]/span[1]').get_attribute('textContent')
        time = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[1]/p[4]').get_attribute('textContent')
        date_time = f'{month}_{week}_{time}'

        home_team = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[2]/div[1]/div[1]/p[1]').get_attribute('textContent')
        away_team = self.driver.find_element_by_xpath('//*[@id="game__top__inner"]/div[2]/div[3]/div[1]/p[1]').get_attribute('textContent')

        # シートのタイトル（このタイトルでシートを作成）
        title = f'{year}_{date_time}_{home_team}vs.{away_team}'

        # シート作成
        worksheet = workbook.add_worksheet(title=title, rows=1000, cols=40)
        return worksheet

    def __write_tbody_contents(self, tbody, thead_row):
        trs = tbody.find_elements_by_tag_name('tr')

        # 各tableのtr要素の子要素であるtdの１行を配列に収める
        # 結果としてtable要素の全ての列が行ごとにまとまって配列となる
        for idx, tr in enumerate(trs):
            tbody_cell_list = self.ws.range(thead_row + idx + 1, 1, thead_row + idx + 1, 27)
            tds = tr.find_elements_by_tag_name('td')
            td_rows_data = []
            one_row_data = self.__extract_tbody_one_row(tds)
            td_rows_data.append(one_row_data)
            
            # １行ごとにgoole sheetのvlaueを更新していく処理
            for i, cell in enumerate(tbody_cell_list):
                cell.value = one_row_data[i]
            self.ws.update_cells(tbody_cell_list, value_input_option='USER_ENTERED')

        # 上記処理で１配列に収めた複数行のtableデータをそれぞれのcellに収める処理
        # for cell, td_data in zip(tbody_cell_list, td_rows_data):
        #     cell.value = td_data
        # self.ws.update_cells(tbody_cell_list, value_input_option='USER_ENTERED')

    def __extract_tbody_one_row(self, tds):
        one_row_data = []

        if '・' in tds[2].get_attribute('textContent'):
            # 外人選手の場合    
            # 海外選手のファミリーネームが2重になっているので削除
            name_data = tds[2].get_attribute('textContent')
            delete_word_count = len(name_data.split('・')[1])/2
            last_word = len(name_data) - delete_word_count
            name = name_data[0:int(last_word)]
        else:
            # 日本人選手の場合
            name_data = tds[2].get_attribute('textContent')
            delete_word_count = len(name_data.split(' ')[0])
            last_word = len(name_data) - delete_word_count
            name = name_data[0:int(last_word)]

        for idx, each_cell_data in enumerate(tds):
            if idx == 2:
                cell_data = name
            else:
                cell_data = each_cell_data.get_attribute('textContent')
            one_row_data.append(cell_data)
        return one_row_data