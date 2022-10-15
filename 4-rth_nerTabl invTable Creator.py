from datetime import datetime
import os
import pandas as pd
import csv

start_time = datetime.now()

dir_name = "/home/esquattro/DH_tolstoy/testhere"
test = os.listdir(dir_name)

header_ner_tabl = ['NE', 'NE_id', 'NE_index']
rows_ner_tabl = []

header_inv_tabl = ['NE', 'Success_binary']
rows_inv_tabl = []

nerTabl = pd.read_csv("resultTable.csv", sep=',')
invTabl = pd.read_csv("tablerev.tsv", sep='\t')
# Volume = 9, ID = 10
# =3, >=4, <=5
for row in nerTabl.itertuples():
    for line in invTabl.itertuples():
        if row[9] == line[3]:
            if row[10] >= line[3]:
                if row[10] <= line[5]:
                    one_ner_row = []
                    one_ner_row = [row[3], line[1], line[2]]
                    rows_ner_tabl.append(one_ner_row)

                    one_inv_row = []
                    one_inv_row = [line[2], '1']
                    rows_inv_tabl.append(one_inv_row)
                else:
                    one_inv_row = []
                    one_inv_row = [line[2], '0']
                    rows_inv_tabl.append(one_inv_row)
            else:
                one_inv_row = []
                one_inv_row = [line[2], '0']
                rows_inv_tabl.append(one_inv_row)

with open('nerTabl.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header_ner_tabl)
    writer.writerows(rows_ner_tabl)

with open('invTabl.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header_inv_tabl)
    writer.writerows(rows_inv_tabl)

# часть 3 из тз, дополнение NerTabl данными из InvertTabl
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
