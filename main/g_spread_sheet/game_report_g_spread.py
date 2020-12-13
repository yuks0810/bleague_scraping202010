import time
class GameReportGSpread:
    def __init__(self, driver=None, url=None, delete=False):
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

    def get_game_url(self):
        self.ws.update_acell('C1', "対象ページURL")
        self.ws.update_acell('C2', self.url)

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

    def write_table(self):
        self.__write_team_names_on_top_of_table()
        self.__get_table_data()
        self.__get_table_footer_date()


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

    def __cellsTo1DArry(self, cells_arry):
        cells1d = []
        for cells in cells_arry:
            cells1d.extend(cells)
        return cells1d

    def __write_team_names_on_top_of_table(self):
        home_team = self.driver.find_element_by_css_selector('.team_wrap.home').get_attribute('textContent').replace('\n', '').replace(' ', '')
        away_team = self.driver.find_element_by_css_selector('.team_wrap.away').get_attribute('textContent').replace('\n', '').replace(' ', '')

        self.ws.update_acell('B9', home_team)
        self.ws.update_acell('F9', away_team)
        time.sleep(2)

    def __get_table_data(self):
        table = self.driver.find_element_by_id("highlight_data")
        trs = table.find_elements_by_tag_name('tr')
        trs_count = len(trs)
        first_row = 10
        cell_list = self.ws.range(f'B{first_row}'+ ":" + f'F{first_row + trs_count}')

        update_cell_arry = []
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            home_team_point = tds[0].get_attribute('textContent')
            away_team_point = tds[2].get_attribute('textContent')

            # 勝った方に矢印を設定する。
            if "win" in tds[0].get_attribute('class').split(' '):
                tmp_arry = [home_team_point, "<", tds[1].get_attribute('textContent'), "", away_team_point ]
            elif "win" in tds[2].get_attribute('class').split(' '):
                tmp_arry = [home_team_point, "", tds[1].get_attribute('textContent'), ">", away_team_point ]
            else:
                tmp_arry = [home_team_point, "", tds[1].get_attribute('textContent'), "", away_team_point ]

            update_cell_arry.append(tmp_arry)
        cells1d_arry = self.__cellsTo1DArry(update_cell_arry)

        for (cell, arry_val) in zip(cell_list, cells1d_arry):
            cell.value = arry_val

        self.ws.update_cells(cell_list, value_input_option='USER_ENTERED')

    def __get_table_footer_date(self):
        # tfooterの上のテーブルに上書きしないように情報を取得
        table = self.driver.find_elements_by_id("highlight_data")[0]
        trs = table.find_elements_by_tag_name('tr')
        trs_count = len(trs)
        first_row = 10
        written_range = f'B{first_row}'+ ":" + f'F{first_row + trs_count}'

        table2 = self.driver.find_elements_by_id("highlight_data")[1]
        trs2 = table2.find_elements_by_tag_name('tr')
        trs2_count = len(trs2)
        trs2_first_row = first_row + trs_count + 1

        cell_list = self.ws.range(f'B{trs2_first_row}' + ":" + f'F{trs2_first_row + trs2_count}')

        update_cell_arry = []
        for tr in trs2:
            tds = tr.find_elements_by_tag_name('td')
            tmp_arry = ["", tds[0].get_attribute('textContent'), "", tds[1].get_attribute('textContent'), ""]
            update_cell_arry.append(tmp_arry)
        cells1d_arry = self.__cellsTo1DArry(update_cell_arry)

        for (cell, arry_val) in zip(cell_list, cells1d_arry):
            cell.value = arry_val

        self.ws.update_cells(cell_list, value_input_option='USER_ENTERED')
        time.sleep(2)