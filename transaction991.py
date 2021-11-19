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
days = []

# extract all unique days
days.append(csvdata[0][2])
for row in csvdata:
        if row[2] not in days:
                days.append(row[2])

# initialize sum of each day
daysum = np.tile(0.0, len(days)+1)

# iterate over the rows to calculate sum for each day
for row in csvdata:
        daysum[int(row[2])] = daysum[int(row[2])] + float(row[4])

# append output
for index, val in enumerate(daysum[1:]): #python starts from 0, this day doesn't exist
        Q1.append([index+1,round(val,2)])

# print results into a file
with open('out/task1.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q1)

#######################
# Option 2: with pandas
#######################
Q1P = []

# get all unique days
daysList = df['transactionDay'].drop_duplicates().tolist()
# convert chars to integers
daysList = map(int, daysList)

# extract from data frame
for day in daysList:
        # get sum for each day
        sumPerDay = df[df['transactionDay'] == day]['transactionAmount'].sum()
        Q1P.append([day, round(sumPerDay,2)])

# print results into a file
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

# get all unique users
users.append(csvdata[0][1])
for row in csvdata:
        if row[1] not in users:
                users.append(row[1])

# get all unique transaction types
trans.append(csvdata[0][3])
for row in csvdata:
        if row[3] not in trans:
                trans.append(row[3])

# initialize matrixes
valOutput = [([0.0]*len(trans)) for i in range(len(users))]
count = [([0]*len(trans)) for i in range(len(users))]

# update matrixes with sum of transactions and count how much it is added in
for row in csvdata:
        idx_user = users.index(row[1])
        idx_trType = trans.index(row[3])
        valOutput[idx_user][idx_trType] += float(row[4])
        count[idx_user][idx_trType] += 1

# get averate and append
for i in range(len(users)):
        a = []
        a.append(users[i])
        for j in range(len(trans)):
                if count[i][j] > 0:
                        valOutput[i][j] = valOutput[i][j] / count[i][j]
                a.append(round(valOutput[i][j],2))
        Q2.append(a)

# print results into a file
with open('out/task2.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q2)

#######################
# Option 2: with pandas
#######################
Q2P = []

# get all unique categories
catList = df['category'].drop_duplicates().tolist()
# get all unique accounts
accList = df['accountId'].drop_duplicates().tolist()

# extract from data frame
for account in accList:
        a = []
        a.append(account)
        # get account average for each transaction type
        for category in catList:
                avgNum = df[(df['accountId'] == account) & (df['category'] == category)]['transactionAmount'].mean()
                a.append(round(avgNum,2))
        Q2P.append(a)

# print results into a file
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

# get all unique days
daysList = df['transactionDay'].drop_duplicates().tolist()

for day in daysList:
        intDay = int(day)
        # get all accounts for this day
        users = df[df['transactionDay'] == intDay]['accountId'].drop_duplicates().tolist()
        for user in users:
                a = []
                # for each account occurance on current day, get particular values
                # get all values for past 5 days before to get max and mean
                outpt = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1)]['transactionAmount']
                # a. get max value of outpt
                max_val = outpt.max()
                # b. get mean value of outpt
                avg_val = outpt.mean()
                # c. get sum of transactions for the past 5 days ('AA' transaction type)
                outAA = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1) & (df['category'] == 'AA')]['transactionAmount'].sum()
                # c. get sum of transactions for the past 5 days ('CC' transaction type)
                outCC = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1) & (df['category'] == 'CC')]['transactionAmount'].sum()
                # c. get sum of transactions for the past 5 days ('FF' transaction type)
                outFF = df[(df['accountId'] == user) & (df['transactionDay'] >= intDay-5) & (df['transactionDay'] <= intDay-1) & (df['category'] == 'FF')]['transactionAmount'].sum()

                a.extend([day,user,round(max_val,2),round(avg_val,2),round(outAA,2),round(outCC,2),round(outFF,2)])
                Q3.append(a)

# print results into a file
with open('out/ptask3.csv', 'w', newline='') as out_f:
    w = csv.writer(out_f, delimiter=',')
    w.writerows(Q3)
