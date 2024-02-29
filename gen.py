import csv
import random
from faker import Faker

fake = Faker()

data = []
for _ in range(1000):
    hash_value = fake.sha256()
    block = fake.random_int(min=10000000, max=20000000)
    age = fake.date_time_this_decade()
    sender = fake.hexify(text='^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    receiver = fake.hexify(text='^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    value = f"{random.uniform(0.001, 10):.8f} ETH"
    txn_fee = f"{random.uniform(0.001, 0.01):.8f}"

    data.append([hash_value, block, age, sender, receiver, value, txn_fee])

csv_file_path = "random_dataset.csv"
header = ["Hash", "Block", "Age", "From", "To", "Value", "Txn Fee"]

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)

