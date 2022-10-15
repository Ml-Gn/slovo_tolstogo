import os
import pandas as pd
from datetime import datetime

start_time = datetime.now()

# задаем рабочую директорию с файлами
dir_name = "/home/esquattro/DH_tolstoy/testhere"
test = os.listdir(dir_name)

header = []
rows = []

df_NET = pd.read_csv("NamedEntsTest.csv", sep=',')
df_PVI = pd.read_csv("PageVolumeIdsTest.csv", sep=',')
result = pd.merge(df_NET, df_PVI, how="left", on=['fileName', 'namedEntity'])
result.to_csv('resultTable.csv')

# получаем таблицу где соединены именованные сущности и тома/страницы


end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
