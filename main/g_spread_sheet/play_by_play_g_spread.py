import time
class PlayByPLayGSpread:
    def __init__(self, driver=None, url=None, delete=False):
        super().__init__()
        import json

        # ここでjsonfile名と2-2で用意したkeyを入力
        self.driver = driver
        self.jsonf = "dynamic-density-293202-cfdad7f5ab26.json"
        self.spread_sheet_key = "1sKvBT8vjL89CXyQkvRxohX-e9qkjaWoqexwJ9f-2AyE"

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
        self.__get_play_by_play_data("1Q")
        time.sleep(2)
        self.__get_play_by_play_data("2Q")
        time.sleep(2)
        self.__get_play_by_play_data("3Q")
        time.sleep(2)
        self.__get_play_by_play_data("4Q")


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

    def __get_play_by_play_data(self, quater_num):
        # liにunvisibleクラスを持っているものは表示されていないので抜いてカウント
        Q1_visible_len_count, Q1_visible_lis, Q2_visible_len_count, Q2_visible_lis, Q3_visible_len_count, Q3_visible_lis, Q4_visible_len_count, Q4_visible_lis = self.__get_each_qater_len()

        init_row = 10

        if quater_num == "1Q":
            self.ws.update_acell('H8', "1Q")
            first_row = init_row
            cell_list = self.ws.range(f'B{first_row}:N{Q1_visible_len_count}')
            visible_lis = Q1_visible_lis
        elif quater_num == "2Q":
            first_row = init_row + Q1_visible_len_count + 6
            self.ws.update_acell(f'H{first_row - 3}', "2Q")
            cell_list = self.ws.range(f'B{first_row}:N{Q2_visible_len_count}')
            visible_lis = Q2_visible_lis
        elif quater_num == "3Q":
            first_row = init_row + Q1_visible_len_count + 6 + Q2_visible_len_count + 6
            self.ws.update_acell(f'H{first_row - 3}', "3Q")
            cell_list = self.ws.range(f'B{first_row}:N{Q3_visible_len_count}')
            visible_lis = Q3_visible_lis
        elif quater_num == "4Q":
            first_row = init_row + Q1_visible_len_count + 6 + Q2_visible_len_count + 6 + Q3_visible_len_count + 6
            self.ws.update_acell(f'H{first_row - 3}', "4Q")
            cell_list = self.ws.range(f'B{first_row}:N{Q4_visible_len_count}')
            visible_lis = Q4_visible_lis

        update_cell_arry = []
        for li in visible_lis:

            time_point_wrap = li.find_element_by_class_name('time_point_wrap').find_element_by_tag_name('p').get_attribute('textContent')
            player_date = li.find_element_by_class_name('player_data').find_element_by_tag_name('p').get_attribute('textContent')

            home_arry = []
            middle_arry = []
            home_arryaway_arry = []

            li_classes = li.get_attribute('class').split(' ')

            if 'away' in li_classes:
                home_arry = ["", "", "", "", "", ""]
                middle_arry = [time_point_wrap]
                away_arry = player_date.split(' ')

                if len(away_arry) < 6:
                    for times in range(6 - len(away_arry)):
                        away_arry.append('')
            elif 'home' in li_classes:
                home_arry = player_date.split(' ')
                middle_arry = [time_point_wrap]
                away_arry = ["", "", "", "", "", ""]

                if len(home_arry) < 6:
                    for times in range(6 - len(home_arry)):
                        home_arry.append('')

            one_row = home_arry + middle_arry + away_arry
            update_cell_arry.append(one_row)

        # 配列を1次元にする
        cells1d_arry = self.__cellsTo1DArry(update_cell_arry)

        for (cell, arry_val) in zip(cell_list, cells1d_arry):
            cell.value = arry_val

        self.ws.update_cells(cell_list, value_input_option='USER_ENTERED')
        time.sleep(4)

    def __visible_li_count(self, Q_ul):
        lis = Q_ul.find_elements_by_tag_name('li')

        visible_lis = []
        for li in lis:
            li_class = li.get_attribute('class').split(' ')
            if not "unvisible" in li_class:
                visible_lis.append(li)

        visible_len_count = len(visible_lis)
        return visible_len_count, visible_lis

    def __get_each_qater_len(self):
        Q1_ul = self.driver.find_element_by_xpath('//*[@id="game__playbyplay__inner"]/ul[3]/li[4]/ul')
        Q1_visible_len_count, Q1_visible_lis = self.__visible_li_count(Q1_ul)
        Q2_ul = self.driver.find_element_by_xpath('//*[@id="game__playbyplay__inner"]/ul[3]/li[3]/ul')
        Q2_visible_len_count, Q2_visible_lis = self.__visible_li_count(Q2_ul)
        Q3_ul = self.driver.find_element_by_xpath('//*[@id="game__playbyplay__inner"]/ul[3]/li[2]/ul')
        Q3_visible_len_count, Q3_visible_lis = self.__visible_li_count(Q3_ul)
        Q4_ul = self.driver.find_element_by_xpath('//*[@id="game__playbyplay__inner"]/ul[3]/li[1]/ul')
        Q4_visible_len_count, Q4_visible_lis = self.__visible_li_count(Q4_ul)

        return Q1_visible_len_count, Q1_visible_lis, Q2_visible_len_count, Q2_visible_lis, Q3_visible_len_count, Q3_visible_lis, Q4_visible_len_count, Q4_visible_lis,
