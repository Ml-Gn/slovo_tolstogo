from datetime import datetime
from navec import Navec
from slovnet import NER
import os
import csv
from bs4 import BeautifulSoup
import pandas as pd
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
header = ['fileName', 'namedEntity', 'NE_type',
          'NE_normalized', 'start', 'stop', 'context']
rows = []
# Цикл для файлов в папке тест

verifier = pd.read_csv("results_updated_works.csv",
                       sep=',', header=None, skiprows=1)
# название файла зависит от папки в которой исполняется файл
# для азбуки будет соответственно results_azbuka.csv
filesColumn = verifier[0].astype("str").values.tolist()
for file in test:
    if file in filesColumn:
        print('successfully found', file)
        xml_file = open(file, 'r').read()
        soup = BeautifulSoup(xml_file, "xml")
        textWithPagesIDS = soup.div.text
        str_textWithPagesIDS = str(textWithPagesIDS)
        doc = Doc(str_textWithPagesIDS)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        doc.parse_syntax(syntax_parser)
        final = doc.tag_ner(ner_tagger)

        for span in doc.spans:
            counter = span.start
            finalStart = counter - 140
            if finalStart < 0:
                finalStart = 0
            second_counter = span.stop
            finalStop = second_counter + 140
            if finalStop > len(str_textWithPagesIDS):
                finalStop = len(str_textWithPagesIDS)
            span.normalize(morph_vocab)
            one_row = []
            one_row = [file, span.text, span.type, span.normal, span.start,
                       span.stop, str_textWithPagesIDS[finalStart: finalStop]]
            rows.append(one_row)


with open('NamedEntsTest.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)
# получаем таблицу именованных сущностей из текста без тегов

# засекает время исполнения
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
