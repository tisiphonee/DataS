from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re

BLOCK = 10
PAGE_LOAD = 100

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

options = webdriver.FirefoxOptions()
#options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # no GUI#
#driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(options=options)


block_counter = 0
page_counter = 1
prev = []

hash_list = []
block_list = []
age_list = []
from_list = []
to_list = []
value_list = []
txn_fee_list = []
    
while(block_counter != BLOCK + 1):
    url = 'https://etherscan.io/txs?ps=' + str(PAGE_LOAD) +'&p=' + str(page_counter)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('tbody')
    rows = table.find_all('tr')[1:]  

    
    
    for row in rows[:100]:
        columns = row.find_all('td')    
        current_block = columns[3].text.strip()
        
        if(current_block not in prev):
            prev.append(current_block)
            block_counter += 1
        
        if(block_counter > BLOCK + 1):
            break;
        
        hash_list.append(columns[1].text.strip())
        block_list.append(current_block)
        age_list.append(columns[5].text.strip())
        from_list.append(extract_wallet_address(columns[7]))
        to_list.append(extract_wallet_address(columns[9]))
        value_list.append(columns[10].text.strip())
        txn_fee_list.append(columns[11].text.strip())
        
    page_counter += 1

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
