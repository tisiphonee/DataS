from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

# options = webdriver.FirefoxOptions()
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # no GUI
driver = webdriver.Chrome(options=options)
# driver = webdriver.Firefox(options=options)


url = 'https://etherscan.io/txs'

driver.get(url)

time.sleep(0.5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('tbody')
rows = table.find_all('tr', limit=11)[1:]  

hash_list = []
block_list = []
age_list = []
from_list = []
to_list = []
value_list = []
txn_fee_list = []

for row in rows[:10]:
    columns = row.find_all('td')
    hash_list.append(columns[1].text.strip())
    block_list.append(columns[3].text.strip())
    age_list.append(columns[5].text.strip())
    from_list.append(columns[7].text.strip())
    to_list.append(columns[9].text.strip())
    value_list.append(columns[10].text.strip())
    txn_fee_list.append(columns[11].text.strip())

df = pd.DataFrame({
    'Hash': hash_list,
    'Block': block_list,
    'Age': age_list,
    'From': from_list,
    'To': to_list,
    'Value': value_list,
    'Txn Fee': txn_fee_list
})


driver.quit()
df.to_csv('output.csv', index=False)
