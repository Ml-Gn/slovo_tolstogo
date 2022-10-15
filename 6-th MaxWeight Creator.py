from datetime import datetime
import pandas as pd
import csv

start_time = datetime.now()

header_weight_tabl = ['NE_index, NE_id, NE_normalized, weight, named_entity,'
                      'NE_type, start_loc, stop_loc, file_name']
# fresh fixes перенос пробелов
rows_max_weight_tabl = []

weightTabl = pd.read_csv("weightTabl.csv", sep=',', header=None, skiprows=1)
for row in weightTabl.itertuples():
    if row[4] == 1:
        one_weight_row = []
        one_weight_row = [row[1], row[2], row[3], row[4], row[5],
                          row[6], row[7], row[8], row[9]]
        rows_max_weight_tabl.append(one_weight_row)

with open('maxWeightTabl.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header_weight_tabl)
    writer.writerows(rows_max_weight_tabl)

# Создаем таблицу с максимальными весами
# Неактуально если вы закомментили else в прошлом файле
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
