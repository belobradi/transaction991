import csv
import os
import numpy as np
import pandas as pd
from numpy.lib.function_base import append

# Create "out" directory if needed
dirName = 'out'
try:
    os.mkdir(dirName)
    print("Directory " , dirName ,  " created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

# Read from file
in_f = open('in/transactions.txt')

csvreader = csv.reader(in_f)
csvheader = next(csvreader)

csvdata = []
for row in csvreader:
        csvdata.append(row)
in_f.close

# Question 1:
# Calculate the total transaction value for all transactions for each day.
# The output should contain one line for each day and each line should include the day and the total value

i=0
Q1 = []
daysum = np.tile(0.0, 30)

for row in csvdata:
        daysum[int(row[2])] = daysum[int(row[2])] + float(row[4])

for index, val in enumerate(daysum[1:]):
        Q1.append([index+1,round(val,2)])

with open('out/task1.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q1)


# Question 2:
# Calculate the average value of transactions per account for each type of transaction (there are seven in total).
# The output should contain one line per account, each line should include the account id and the average
# value for each transaction type (ie 7 fields containing the average values).

transType = ['AA','BB','CC','DD','EE','FF','GG']
users = []
Q2 = []

users.append(csvdata[0][1])
for row in csvdata:
        if row[1] not in users:
                users.append(row[1])

valOutput = [([0.0]*len(transType)) for i in range(len(users))]
count = [([0]*len(transType)) for i in range(len(users))]

for row in csvdata:
        idx_user = users.index(row[1])
        idx_trType = transType.index(row[3])
        valOutput[idx_user][idx_trType] += float(row[4])
        count[idx_user][idx_trType] += 1


for i in range(len(users)):
        a = []
        a.append(users[i])
        for j in range(len(transType)):
                if count[i][j] > 0:
                        valOutput[i][j] = valOutput[i][j] / count[i][j]
                a.append(round(valOutput[i][j],2))
        Q2.append(a)

with open('out/task2.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q2)

# For each day, calculate statistics for each account number for the previous five days of transactions, not
# including transactions from the day statistics are being calculated for. For example, on day 10 you should
# consider only the transactions from days 5 to 9 (this is called a rolling time window of five days). The
# statistics we require to be calculated are:
# 1. The maximum transaction value in the previous 5 days of transactions per account
# 2. The average transaction value of the previous 5 days of transactions per account
# 3. The total transaction value of transactions types “AA”, “CC” and “FF” in the previous 5 days per
#    account

days = []
days.append(csvdata[0][2])
for row in csvdata:
        if row[2] not in days:
                days.append(row[2])

df = pd.read_csv('in/transactions.txt')
print(df)

Q3 = []
for day in days:
        intDay = int(day)
        output = df[df['transactionDay'] == intDay]['accountId']
        users = output.drop_duplicates().tolist()
        for user in users:
                a = []
                outpt = df[(df['accountId'] == user) & (df['transactionDay'] > intDay-5) & (df['transactionDay'] < intDay)]['transactionAmount']
                outAA = df[(df['accountId'] == user) & (df['transactionDay'] > intDay-5) & (df['transactionDay'] < intDay) & (df['category'] == 'AA')]['transactionAmount']
                outCC = df[(df['accountId'] == user) & (df['transactionDay'] > intDay-5) & (df['transactionDay'] < intDay) & (df['category'] == 'CC')]['transactionAmount']
                outFF = df[(df['accountId'] == user) & (df['transactionDay'] > intDay-5) & (df['transactionDay'] < intDay) & (df['category'] == 'FF')]['transactionAmount']
                max_val = outpt.max()
                avg_val = outpt.mean()
                AA_summ = outAA.sum()
                CC_summ = outCC.sum()
                FF_summ = outFF.sum()
                a.extend([day,user,round(max_val,2),round(avg_val,2),round(AA_summ,2),round(CC_summ,2),round(FF_summ,2)])
                Q3.append(a)

with open('out/task3.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q3)