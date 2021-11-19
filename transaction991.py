import csv
import os
import numpy as np
import pandas as pd
from numpy.lib.function_base import append

##################################
# Create "out" directory if needed
##################################
dirName = 'out'
try:
        # directory doesn't exist
        os.mkdir(dirName)
        print("Directory " , dirName ,  " created ") 
except FileExistsError:
        # directory exists
        print("Directory " , dirName ,  " already exists")

################################
# Option 1: Read CSV into a list
################################
in_f = open('in/transactions.txt')
csvreader = csv.reader(in_f)

# read header
csvheader = next(csvreader)

# read data
csvdata = []
for row in csvreader:
        csvdata.append(row)
in_f.close

#################################
# Option 2: Read CSV using pandas
#################################
df = pd.read_csv('in/transactions.txt')
print(df)

##########################################################################################################
# Question 1:
# Calculate the total transaction value for all transactions for each day.
# The output should contain one line for each day and each line should include the day and the total value
##########################################################################################################
# Option 1: without pandas
##########################
Q1 = []

daysum = np.tile(0.0, 30)

for row in csvdata:
        daysum[int(row[2])] = daysum[int(row[2])] + float(row[4])

for index, val in enumerate(daysum[1:]):
        Q1.append([index+1,round(val,2)])

with open('out/task1.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q1)

#######################
# Option 2: with pandas
#######################
Q1P = []

daysList = df['transactionDay'].drop_duplicates().tolist()
daysList = map(int, daysList)

for day in daysList:
        sumPerDay = df[df['transactionDay'] == day]['transactionAmount'].sum()
        Q1P.append([day, round(sumPerDay,2)])

with open('out/ptask1.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q1P)

##################################################################################################################
# Question 2:
# Calculate the average value of transactions per account for each type of transaction (there are seven in total).
# The output should contain one line per account, each line should include the account id and the average
# value for each transaction type (ie 7 fields containing the average values).
##################################################################################################################
# Option 1: without pandas
##########################
Q2 = []
trans = []
users = []

users.append(csvdata[0][1])
for row in csvdata:
        if row[1] not in users:
                users.append(row[1])

trans.append(csvdata[0][3])
for row in csvdata:
        if row[3] not in trans:
                trans.append(row[3])

valOutput = [([0.0]*len(trans)) for i in range(len(users))]
count = [([0]*len(trans)) for i in range(len(users))]

for row in csvdata:
        idx_user = users.index(row[1])
        idx_trType = trans.index(row[3])
        valOutput[idx_user][idx_trType] += float(row[4])
        count[idx_user][idx_trType] += 1

for i in range(len(users)):
        a = []
        a.append(users[i])
        for j in range(len(trans)):
                if count[i][j] > 0:
                        valOutput[i][j] = valOutput[i][j] / count[i][j]
                a.append(round(valOutput[i][j],2))
        Q2.append(a)

with open('out/task2.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q2)

#######################
# Option 2: with pandas
#######################
Q2P = []

catList = df['category'].drop_duplicates().tolist()
accList = df['accountId'].drop_duplicates().tolist()

for account in accList:
        a = []
        a.append(account)
        for category in catList:
                avgNum = df[(df['accountId'] == account) & (df['category'] == category)]['transactionAmount'].mean()
                a.append(round(avgNum,2))
        Q2P.append(a)

with open('out/ptask2.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q2P)

############################################################################################################
# For each day, calculate statistics for each account number for the previous five days of transactions, not
# including transactions from the day statistics are being calculated for. For example, on day 10 you should
# consider only the transactions from days 5 to 9 (this is called a rolling time window of five days). The
# statistics we require to be calculated are:
# 1. The maximum transaction value in the previous 5 days of transactions per account
# 2. The average transaction value of the previous 5 days of transactions per account
# 3. The total transaction value of transactions types “AA”, “CC” and “FF” in the previous 5 days per
#    account
############################################################################################################
# Option 1: without pandas
##########################

# I could do this with pointers and logic, but our eyes would start to bleed and I'd need more than a week.

#######################
# Option 2: with pandas
#######################
Q3 = []

daysList = df['transactionDay'].drop_duplicates().tolist()

for day in daysList:
        intDay = int(day)
        users = df[df['transactionDay'] == intDay]['accountId'].drop_duplicates().tolist()
        for user in users:
                a = []
                outpt = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1)]['transactionAmount']
                outAA = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1) & (df['category'] == 'AA')]['transactionAmount'].sum()
                outCC = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1) & (df['category'] == 'CC')]['transactionAmount'].sum()
                outFF = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1) & (df['category'] == 'FF')]['transactionAmount'].sum()
                max_val = outpt.max()
                avg_val = outpt.mean()
                a.extend([day,user,round(max_val,2),round(avg_val,2),round(outAA,2),round(outCC,2),round(outFF,2)])
                Q3.append(a)

with open('out/ptask3.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q3)
