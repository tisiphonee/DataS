from scipy.stats import skew, kurtosis, norm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import random

# Assuming df is your DataFrame and "block" is your column of interest.
# Adjust the frac parameter as needed. In this case, 0.1 will give 10%.
def sample_from_each_group(group):
    return group.sample(frac=0.1, random_state = random.randint(1, 1000000))

df = pd.read_csv('random_dataset.csv')
df = df.groupby('Block').apply(sample_from_each_group)


# Reset the index if needed
df = df.reset_index(drop=True)
df.to_csv("SSoutput.csv")

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


skewness_value = skew(df['Value'])
kurtosis_value = kurtosis(df['Value'])

print(f"Value Skewness Value: {skewness_value}")
print(f"Value Kurtosis Value: {kurtosis_value}")

skewness_value = skew(df['Txn Fee'])
kurtosis_value = kurtosis(df['Txn Fee'])

print(f"Value Skewness Txn Fee : {skewness_value}")
print(f"Value Kurtosis Txn Fee: {kurtosis_value}")

plt.figure(figsize=(8, 5))

plt.subplot(1, 2, 1)
sns.histplot(df['Txn Fee'], bins=int(math.sqrt(len(df['Txn Fee']))),kde=True, color='g', alpha=0.7)
mu, std = df['Txn Fee'].mean(), df['Txn Fee'].std()
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std) 
plt.plot(x, p, 'k', linewidth=3)
plt.title('Txn Fee Distribution with Normal Fit')
plt.xlabel('Txn Fee')

plt.subplot(1, 2, 2)
sns.histplot(df['Value'], bins=int(math.sqrt(len(df['Value']))),kde=True, color='b', alpha=0.7)
mu, std = df['Value'].mean(), df['Value'].std()
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=3)
plt.title('Value Distribution with Normal Fit')
plt.xlabel('Value')
plt.ylim(bottom=0)

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

sns.boxplot(x=df['Txn Fee'], ax=axes[0, 0])
axes[0, 0].set_title('Box Plot - Txn Fee')

sns.violinplot(x=df['Txn Fee'], ax=axes[1,0])
axes[1,0].set_title('Violin Plot - Txn Fee')

sns.boxplot(x=df['Value'], ax=axes[0, 1])
axes[0, 1].set_title('Box Plot - Value')

sns.violinplot(x=df['Value'], ax=axes[1, 1])
axes[1, 1].set_title('Violin Plot - Value')

plt.tight_layout()
plt.show()
