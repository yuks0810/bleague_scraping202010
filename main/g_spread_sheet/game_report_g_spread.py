class GameReportGSpread:

    def __init__(self, driver):
        super().__init__()
        import json

        # ここでjsonfile名と2-2で用意したkeyを入力
        self.driver = driver
        self.jsonf = "dynamic-density-293202-cfdad7f5ab26.json"
        self.spread_sheet_key = "1HjPQNCtO6WWCsrFEOCehemHwqj2C-35IbX-wZBPMbGc"
        self.ws = self.__connect_gspread(self.jsonf, self.spread_sheet_key)
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
    
    def write_thead(self):
        # theads = []
        # theads.append(self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[1]/table/thead'))
        # theads.append(self.driver.find_element_by_xpath('//*[@id="game__boxscore__inner"]/ul[2]/li[1]/div[2]/table/thead'))
        theads = self.driver.find_elements_by_tag_name('thead')
        tbodies = self.driver.find_elements_by_tag_name('tbody')

        for idx, thead in enumerate(theads):
            # if idx > 4:
            if idx == 0:
                cell_list = self.ws.range(6, 1, 6, 26)
            else:
                cell_list = self.ws.range(idx * 23, 1, idx * 23, 26)

            ths = thead.find_element_by_tag_name('tr').find_elements_by_tag_name('th')
            for i, cell in enumerate(cell_list):
                val = ths[i].get_attribute("textContent")
                cell.value = val
                
            self.ws.update_cells(cell_list, value_input_option='USER_ENTERED')
            self.__write_tbody_contents(tbodies[idx])
        

    ## private 

    def __connect_gspread(self, jsonf,key):
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials

        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = key
        worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
        return worksheet

    def __write_tbody_contents(self, tbody):
        trs = tbody.find_elements_by_tag_name('tr')
        for idx, tr in enumerate(trs):
            tds = tr.find_elements_by_tag_name('td')
            td_data = []
            for td in tds:
                tmp_td = []
                tmp_td.append(td.get_attribute("textContent"))
            td_data.append(tmp_td)
        
        for td_d in td_data:
            self.ws.append_row(td_d)

