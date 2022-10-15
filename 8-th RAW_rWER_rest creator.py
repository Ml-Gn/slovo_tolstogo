from datetime import datetime
from navec import Navec
from slovnet import NER
import os
import csv
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    NamesExtractor,

    Doc
)
start_time = datetime.now()

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)


# задаем рабочую директорию с файлами
dir_name = "/home/esquattro/DH_tolstoy/testhere"
test = os.listdir(dir_name)
# подготовка к использованию словнет-а, указать путь к дх толстой в консоли
path = 'navec_news_v1_1B_250K_300d_100q.tar'
navec = Navec.load(path)
ner = NER.load('slovnet_ner_news_v1.tar')
ner.navec(navec)
# заготовка для таблицы
header = ['fileName', 'namedEntity', 'NE_start_raw', 'NE_stop_raw']
rows = []
# Цикл для файлов в папке тест

verifier = pd.read_csv("results_updated_works.csv", sep=',',
                       header=None, skiprows=1)

files_column = verifier[0].astype("str").values.tolist()
for file in test:
    if file in files_column:
        print('successfully found')
        xml_file = open(file, 'r').read()
        soup = BeautifulSoup(xml_file, "xml")
        str_soup = str(soup)
        doc = Doc(str_soup)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        doc.parse_syntax(syntax_parser)
        final = doc.tag_ner(ner_tagger)

        for span in doc.spans:
            one_row = []
            one_row = [file, span.text, span.start, span.stop]
            rows.append(one_row)


with open('RAW_NamedEntsTest.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

df_r_WET = pd.read_csv("resultWeightEntityTable.csv", sep=',')

df_RAW = pd.read_csv("RAW_NamedEntsTest.csv", sep=',')

df_r_WET = df_r_WET.drop_duplicates(subset=['start_loc'])
df_r_WET['counter'] = df_r_WET.groupby('namedEntity')['fileName'].cumcount()
df_r_WET['namedEntity'] = np.where(df_r_WET['counter'] > 0,
                                   df_r_WET['namedEntity'] +
                                   df_r_WET['counter'].astype(str),
                                   df_r_WET['namedEntity'].astype(str))

df_RAW['counter'] = df_RAW.groupby('namedEntity')['fileName'].cumcount()
df_RAW['namedEntity'] = np.where(df_RAW['counter'] > 0,
                                 df_RAW['namedEntity'] +
                                 df_RAW['counter'].astype(str),
                                 df_RAW['namedEntity'].astype(str))

result = pd.merge(df_r_WET, df_RAW, how="left", on=['namedEntity'])
result.to_csv('RAW_rWET_resultTable.csv')

# соединяем таблицу для получения таблицы с весами, контекстами
# номером символа в очищенном файле и в неочищенном

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
