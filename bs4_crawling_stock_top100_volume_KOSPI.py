from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from datetime import datetime


html_naver_stock_volume_top10 = 'https://finance.naver.com/sise/sise_quant.naver'

req = Request(html_naver_stock_volume_top10)
res = urlopen(req)

html = res.read().decode('cp949')
soup = BeautifulSoup(html, 'html.parser')
table = soup.find("table", { "class" : "type_2" })

rows = table.find_all('tr')

data = []
col_data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])  # Get rid of empty values

for row in rows:
    cols = row.find_all('th')
    cols = [ele.text.strip() for ele in cols]
    if cols:
        col_data.append([ele for ele in cols if ele])  # Get rid of empty values


df_data = pd.DataFrame(data).dropna()
df_data.columns = col_data[0]
df_data = df_data.set_index('N')
today = str(datetime.today()).split('.')[0]
today = today.replace(' ', '_').replace(':', '-')
save_file_name = 'volume_top_100_korea_stock_' + today + '.csv'

df_data.to_csv(save_file_name, encoding='cp949')
