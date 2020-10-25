import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# (1) Google Spread Sheetsにアクセス
def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    return worksheet

# ここでjsonfile名と2-2で用意したkeyを入力
jsonf = "dynamic-density-293202-cfdad7f5ab26.json"
spread_sheet_key = "1sKvBT8vjL89CXyQkvRxohX-e9qkjaWoqexwJ9f-2AyE"
ws = connect_gspread(jsonf,spread_sheet_key)

#(2) Google Spread Sheets上の値を更新
#(２−１)あるセルの値を更新（行と列を指定）
ws.update_cell(1,1,"test1")
ws.update_cell(2,1,1)
ws.update_cell(3,1,2)

#(２−２)あるセルの値を更新（ラベルを指定）
ws.update_acell('C1','test2')
ws.update_acell('C2',1)
ws.update_acell('C3',2)

#(2-3)ある範囲のセルの値を更新
ds= ws.range('E1:G3')
ds[0].value = 1
ds[1].value = 2
ds[2].value = 3
ds[3].value = 4
ds[4].value = 5
ds[5].value = 6
ds[6].value = 7
ds[7].value = 8
ds[8].value = 9
ws.update_cells(ds)