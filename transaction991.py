import csv
import numpy as np

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

