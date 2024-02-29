from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re

# options = webdriver.FirefoxOptions()
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # no GUI
driver = webdriver.Chrome(options=options)
# driver = webdriver.Firefox(options=options)


url = 'https://etherscan.io/txs'

driver.get(url)

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

def extract_wallet_address(column):
    pattern = r"\((0x[0-9a-fA-F]+)\)"
    match = re.search(pattern, str(column))

    if match:
        wallet_address = match.group(1)
    else:
        pattern2 = r"data-clipboard-text=\"0x[0-9a-fA-F]+"
        match = re.search(pattern2, str(column))

        if match:
            wallet_address = match.group().replace('data-clipboard-text=\"', '')
        else:
            wallet_address = None
            
    return wallet_address

for row in rows[:10]:
    columns = row.find_all('td')
    hash_list.append(columns[1].text.strip())
    block_list.append(columns[3].text.strip())
    age_list.append(columns[5].text.strip())
    from_list.append(extract_wallet_address(columns[7]))
    to_list.append(extract_wallet_address(columns[9]))
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
