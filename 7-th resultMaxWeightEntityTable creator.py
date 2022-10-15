from datetime import datetime
import pandas as pd

start_time = datetime.now()

dir_name = "/home/esquattro/DH_tolstoy/testhere"

header = []
rows = []

df_NET = pd.read_csv("resultTable.csv", sep=',')
df_PVI = pd.read_csv("maxWeightTabl.csv", sep=',')
df_NET.drop('Unnamed: 0', inplace=True, axis=1)
print('resultTable', df_NET.columns.tolist())
print('maxWeightTabl', df_PVI.columns.tolist())

result = pd.merge(df_NET, df_PVI.drop_duplicates(), how="inner",
                  left_on=['start_loc'], right_on=['start_loc'])
result.drop_duplicates().to_csv('resultWeightEntityTable.csv')
# Соединяем таблицу с макс весом с результатами

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
