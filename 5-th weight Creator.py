from datetime import datetime
import os
import pandas as pd
import csv

start_time = datetime.now()

# Аккуратно! Этот файл может выполняться очень долго (12 часов +)
# Размер получаемого файла будет несколько гигабайт

header_weight_tabl = ['NE_index, NE_id, NE_normalized, weight, named_entity,'
                      'NE_type, start_loc, stop_loc, file_name']
# fresh fix possible mistake
rows_weight_tabl = []

dir_name = "/home/esquattro/DH_tolstoy/testhere"
test = os.listdir(dir_name)

fullWeight = '1'  # all tokens
partlyWeight = '2'  # two and more
smallWeight = '3'  # first only
noneWeight = '4'  # None

nerTabl = pd.read_csv("nerTabl.csv", sep=',')
resTabl = pd.read_csv("resultTable.csv", sep=',')


def write_to_table(weight):
    one_weight_row = []
    one_weight_row = [NE_index, NE_id, NE_normalized, weight, named_entity,
                      NE_type, start_loc, stop_loc, file_name]
    rows_weight_tabl.append(one_weight_row)


for row in resTabl.itertuples():
    for line in nerTabl.itertuples():

        NE_normalized = row[5]
        named_entity = row[3]
        file_name = row[2]
        start_loc = row[6]
        stop_loc = row[7]
        NE_type = row[4]

        NE_index = line[3]
        NE_id = line[2]
        splitted_index = NE_index.split()
        splitted_normalized = NE_normalized.split()

        if NE_index == NE_normalized:
            write_to_table(fullWeight)
        else:  # Этот else можно закомментить для экономии ресурсов
            words_counter = 0
            for word in splitted_index:
                if word in splitted_normalized:
                    words_counter += 1
                if words_counter >= 2:
                    write_to_table(partlyWeight)
                    break
            if words_counter == 1:
                if splitted_index[0] == splitted_normalized[0]:
                    write_to_table(smallWeight)
            if words_counter == 0:
                write_to_table(noneWeight)

with open('weightTabl.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header_weight_tabl)
    writer.writerows(rows_weight_tabl)
# получаем таблицу с весами именованных сущностей
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
