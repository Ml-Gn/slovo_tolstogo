from datetime import datetime
from navec import Navec
from slovnet import NER
import os
import re
# import csv
from bs4 import BeautifulSoup
import pandas as pd
# import xml.etree.ElementTree as ET
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    # PER,
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

dir_name = "/home/esquattro/DH_tolstoy/testhere"
test = os.listdir(dir_name)
# подготовка к использованию словнет-а, указать путь к дх толстой в консоли
path = 'navec_news_v1_1B_250K_300d_100q.tar'
navec = Navec.load(path)
ner = NER.load('slovnet_ner_news_v1.tar')
ner.navec(navec)

verifier = pd.read_csv("results_updated_works.csv", sep=',',
                       header=None, skiprows=1)
filesColumn = verifier[0].astype("str").values.tolist()



raw_wet_rtable = pd.read_csv("RAW_rWET_resultTable.csv", sep=',')
rwr_df = raw_wet_rtable.iloc[: , 2:]
# Было 1
clean_rwr = rwr_df.drop_duplicates(subset=['NE_start_raw'])


for file in test:
    if file in filesColumn:
        print('-------------')
        print('successfully found', file)
        print('-------------')
        xml_file = open(file, 'r+')
        soup = BeautifulSoup(xml_file, "xml")
        str_soup = str(soup)
        textWithPagesIDS = soup.div.text
        str_textWithPagesIDS = str(textWithPagesIDS)
        doc = Doc(str_textWithPagesIDS)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        doc.parse_syntax(syntax_parser)
        final = doc.tag_ner(ner_tagger)
        counter = []  # Список который мы пополняем тегами в которые заворачиваем слова
                    # для уточнения номера символа

        for row in clean_rwr.itertuples():
            for span in doc.spans:
                starter = row[5]
                # Задаем значение NE_type для тега
                if row[3] == 'LOC':
                    NE_type = 'type="place"'
                elif row[3] == 'PER':
                    NE_type = 'type="person"'
                else:
                    NE_type = ''
                NE_id = row[11]  # id Именованной сущности
                if span.start == starter:
                    # print('span found successfully')
                    print(row[2], '==', span.text, 'success')
                    print(row[5], '==', span.start, 'success')
                    # print('found starter = line(5)')
                    start_loc = row[20]
                    print('----------------')
                    print(start_loc, 'start loc')
                    end_loc = row[21]
                    print(end_loc, 'end loc')
                    print(str_soup[start_loc: end_loc], 'str soup start to end')
                    print(span.text, 'span to replace')

                    stringed_span = str(span.text)
                    str_counter = ''.join(counter)
                    counter_start_loc = start_loc + len(str_counter)  # стартовый символ + длина символов в каунтере
                    counter_end_loc = end_loc + len(str_counter)
                    if str_soup[counter_start_loc: counter_end_loc] == span.text:
                        print('absolute truth for: ', span.text)
                    print('counter length:', len(str_counter))
                    print('counter_start_loc', counter_start_loc)
                    print('counter_end_loc', counter_end_loc)
                    print('new start to end', str_soup[start_loc: end_loc])
                    print('------------cycle end--------------')

                    if f'<name {NE_type} ref=\"{NE_id}\"> {span.text} </name>' in str_soup:
                        print('alarm!', "----------", 'alarm!')
                        print('false start for ', span.text)
                        print('alarm!', "----------", 'alarm!')
                        break
                    else:
                        str_soup = re.sub(span.text, fr'<name {NE_type} ref="{NE_id}"> {span.text} </name>', str_soup)
                        counter.append(f"<name {NE_type} ref=\"{NE_id}\"> {span.text} </name>")
                        print('Replaced: ', span.text)
                        print('--------')
                        break

        print(counter)
        with open(f"{file}_MarkedUp.xml", 'w') as final_file:
            final_file.write(str_soup)
            final_file.close()
# Создает размеченный файл с названием file_MarkedUp.xml
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
