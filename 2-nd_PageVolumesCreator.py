from datetime import datetime
import os
import csv
from bs4 import BeautifulSoup
import pandas as pd
import re

start_time = datetime.now()

# задаем рабочую директорию с файлами
dir_name = "/home/esquattro/DH_tolstoy/testhere"
test = os.listdir(dir_name)
verifier = pd.read_csv("results_updated_works.csv", sep=',',
                       header=None, skiprows=1)
verifiedFiles = verifier[0].astype("str").values.tolist()
header = ['fileName', 'namedEntity', 'Volume', 'page']
rows = []
# задаем нужный файл и директорию


def filter_p(tag):
    return tag.has_attr('id')


for file in test:
    # Идем по файлам в директории
    if file in verifiedFiles:
        # Идем по колонке с подтвержденной орфографией
        xml_file = open(file, 'r').read()
        soup = BeautifulSoup(xml_file, "xml")
        textWithPagesIDS = soup.find_all(filter_p)
        str_textWithPagesIDS = str(textWithPagesIDS)
        csvVerify = pd.read_csv("NamedEntsTest.csv", sep=',',
                                header=None, skiprows=1)
        columnNE = csvVerify[1].astype("str").values.tolist()
        # RegExp для вытаскивания томов
        texted_soup = str(soup)
        volumeRE = re.search(
            r"(<biblScope unit=\"volume\">)(\d*?)(<\/biblScope>)", texted_soup)
# r' fresh fix possible mistake
        fileVolume = volumeRE.group(2)
        first_page = soup.find("pb")['n']
        pages = []
        pages.append(first_page)
        for tag in textWithPagesIDS:
            foundIndexes = []
            if tag.pb is not None:
                page = tag.pb.get('n')
                pages.append(page)
                for NamedEntity in columnNE:
                    foundIndex = tag.get_text().find(NamedEntity)
                    if foundIndex != -1 and foundIndex not in foundIndexes:
                        one_row = []
                        one_row = [file, NamedEntity, fileVolume, page]
                        rows.append(one_row)
                        foundIndexes.append(foundIndex)
                        pages.append(page)
            else:
                for NamedEntity in columnNE:
                    foundIndex = tag.get_text().find(NamedEntity)
                    if foundIndex != -1 and foundIndex not in foundIndexes:
                        page = pages[-1]
                        one_row = []
                        one_row = [file, NamedEntity, fileVolume, page]
                        rows.append(one_row)
                        foundIndexes.append(foundIndex)


with open('PageVolumeIdsTest.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)


end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
# Мы получаем файл PageVolumeIdsTest
# В нем лежат айди страниц ИС и номера томов
