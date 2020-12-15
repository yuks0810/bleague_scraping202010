import time
class BoxScoreGSpread:

    def __init__(self, driver=None, href_url=None, delete=False):
        super().__init__()
        import json

        # ここでjsonfile名と2-2で用意したkeyを入力
        self.driver = driver
        self.href_url = href_url
        self.jsonf = "dynamic-density-293202-cfdad7f5ab26.json"
        self.spread_sheet_key = "1LiqrYZy14As1a7JY0Lp2RtDGp3LHQiQ7V-T6OoFp8Dg"

        if delete == False:
            self.ws = self.__connect_gspread(self.jsonf, self.spread_sheet_key)

            # カラムの数が40個なければ作成する
            col_num = self.ws.col_count
            self.ws.add_cols(40 - col_num)

    def get_game_url(self):
        self.ws.update_acell('C1', "対象ページURL")
        self.ws.update_acell('C2', self.href_url)

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
        no1_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[1]/table') # 1つ目のテーブル
        no2_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[2]/table') # 2つ目のテーブル
        no3_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[2]/div[1]/table')
        no4_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[2]/div[2]/table')
        no5_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[3]/div[1]/table')
        no6_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[3]/div[2]/table')
        no7_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[4]/div[1]/table')
        no8_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[4]/div[2]/table')
        no9_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[5]/div[1]/table')
        no10_table = self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[5]/div[2]/table')
        tables = [no1_table, no2_table, no3_table, no4_table, no5_table, no6_table, no7_table, no8_table, no9_table, no10_table]

        first_row = 6
        first_col = 1

        for idx, table in enumerate(tables):
            thead = table.find_element_by_tag_name('thead')
            thead_tr = thead.find_element_by_tag_name('tr') # 1つ目のヘッダーの要素
            tbodies = table.find_element_by_tag_name('tbody')
            tbodies_trs = tbodies.find_elements_by_tag_name('tr')
            tfoots = table.find_element_by_tag_name('tfoot')
            tfoots_trs = tfoots.find_elements_by_tag_name('tr')

            all_table_data =[]
            all_table_data.append(thead_tr)
            for i in tbodies_trs:
                all_table_data.append(i)
            for i in tfoots_trs:
                all_table_data.append(i)

            col_num = len(thead_tr.find_elements_by_tag_name('th')) # カラム数
            row_num = 1 + len(tbodies_trs) + len(tfoots_trs) # 行数
            last_row = first_row + row_num
            # gspread sheetのrangeを取得
            cell_list = self.ws.range(first_row, first_col, last_row, col_num)

            # 扱いやすいようにspread sheetのcellsを２次元配列にする
            cells2darray = self.__cellsto2darray(cell_list, col_num)

            # テーブルのデータをセルに入れている
            idx = 1
            for table_data, cells in zip(all_table_data, cells2darray):
                if idx == 1:
                    dbl_data = table_data.find_elements_by_tag_name('th')
                else:
                    dbl_data = table_data.find_elements_by_tag_name('td')
                idx += 1

                idx_for_cell = 1
                for table_datum, cell in zip(dbl_data, cells):
                    if idx > 2 and idx_for_cell == 3 and idx < row_num:
                        if '・' in table_datum.get_attribute('textContent'):
                            # 外人選手の場合
                            # 海外選手のファミリーネームが2重になっているので削除
                            name_data = table_datum.get_attribute('textContent')
                            delete_word_count = len(name_data.split('・')[1])/2
                            last_word = len(name_data) - delete_word_count
                            name = name_data[0:int(last_word)]
                        else:
                            # 日本人選手の場合
                            name_data = table_datum.get_attribute('textContent')
                            delete_word_count = len(name_data.split(' ')[0])
                            last_word = len(name_data) - delete_word_count
                            name = name_data[0:int(last_word)]
                        cell.value = name
                    else:
                        cell.value = table_datum.get_attribute("textContent")

                    idx_for_cell += 1

            # 2次元配列のままだと書き込めないので、1次元配列に戻す
            cell_list = self.__cellsto1darray(cells2darray)

            # 値をgspread sheetに書き込む
            self.ws.update_cells(cell_list)
            first_row += row_num + 4

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

    ####### private #######

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
            ## theadのすぐしたからtableのコンテンツを開始するために+1している。
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

    def __extract_tbody_one_row(self, tds, tfoot=False):
        one_row_data = []

        if tfoot == True:
            for idx, each_cell_data in enumerate(tds):
                cell_data = each_cell_data.get_attribute('textContent')
                one_row_data.append(cell_data)
            return one_row_data

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

    def __write_tfoot_contents(self, tfoot, tbodies_row_count, thead_row):
        trs = tfoot.find_elements_by_tag_name('tr')

        # 各tableのtr要素の子要素であるtdの１行を配列に収める
        # 結果としてtable要素の全ての列が行ごとにまとまって配列となる
        for idx, tr in enumerate(trs):
            tbody_cell_list = self.ws.range(thead_row + tbodies_row_count + idx + 1, 1, thead_row + tbodies_row_count + idx + 1, 27)
            none_empty_cells = []

            for cell in tbody_cell_list:
                if not cell.value == '':
                    none_empty_cells.append(cell)

            if len(none_empty_cells) > 0:
                idx += 1
                tbody_cell_list = self.ws.range(thead_row + tbodies_row_count + idx + 1, 1, thead_row + tbodies_row_count + idx + 1, 27)

            tds = tr.find_elements_by_tag_name('td')
            td_rows_data = []
            one_row_data = self.__extract_tbody_one_row(tds, tfoot=True)
            td_rows_data.append(one_row_data)
            # １行ごとにgoole sheetのvlaueを更新していく処理
            for i, cell in enumerate(tbody_cell_list):
                cell.value = one_row_data[i]
            self.ws.update_cells(tbody_cell_list, value_input_option='USER_ENTERED')

    def line_count_checker_for_insurance(self, tbody_cell_list, thead_row, tbodies_row_count, idx):
        # 結果と選手の行が重なってしまう場合を考慮
        none_empty_cells = []
        for cell in tbody_cell_list:
            if not cell.value == '':
                none_empty_cells.append(cell)

        if len(none_empty_cells) > 0:
            idx += 1
            tbody_cell_list = self.ws.range(thead_row + tbodies_row_count + idx + 1, 1, thead_row + tbodies_row_count + idx + 1, 27)
            self.line_count_checker_for_insurance(tbody_cell_list, thead_row, tbodies_row_count, idx)
        else:
            return tbody_cell_list

    def __cellsto2darray(self, cells, col):  # colは列の数
        cells2d = []
        for i in range(len(cells) // col):
            cells2d.append(cells[i * col:(i + 1) * col])
        return cells2d

    def __cellsto1darray(self, cells2d):
        cells1d = []
        for cells in cells2d:
            cells1d.extend(cells)
        return cells1d