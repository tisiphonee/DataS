import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import numpy as np
import math
import random


df = pd.read_csv('random_dataset.csv')
sample_size = len(df) // 10
df_simple_sample = df.sample(n = sample_size, random_state=random.randint(1, 10000000))

## Data Cleaning : 
df['Value'] = df['Value'].str.rstrip(' ETH').astype(float)
df['Txn Fee'] = df['Txn Fee'].astype(float)

mean_value = df['Value'].mean()
std_value = df['Value'].std()

mean_txn_fee = df['Txn Fee'].mean()
std_txn_fee = df['Txn Fee'].std()

print(f"Value - Mean: {mean_value}, Standard Deviation: {std_value}")
print(f"Txn Fee - Mean: {mean_txn_fee}, Standard Deviation: {std_txn_fee}")


# num_bins_sturges = int(1 + math.log2(len(df['Value'])))


plt.figure(figsize=(6, 3))
plt.suptitle('Histogram Plot of Txn Fee  and Values', y=1.02) 

plt.subplot(1, 2, 1)
sns.histplot(df['Txn Fee'], bins=int(math.sqrt(len(df['Txn Fee']))), color='g', kde=True, alpha=0.7)
plt.title('Txn Fee Distribution')
plt.xlabel('Txn Fee')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
sns.histplot(df['Value'], bins=int(math.sqrt(len(df['Value']))), color='b', kde=True, alpha=0.7)
plt.title('Value Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
