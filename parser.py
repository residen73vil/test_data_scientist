#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import re

def main(csv):
    re_greatings = re.compile(r"(?:(?:здравствуйт?е?)|(?:добр(?:ый|ое)\s(?:вечер|день|утро|ночь))|(?:(?:день|вечер|утро|ночь)\sдобр(?:ый|ое)))", re.IGNORECASE)
    re_farewells = re.compile(r"(?:(?:до\ свидания)|(?:всего\ доброго)|(?:до\ новых\ встреч)|(?:хорошего (?:дня|вечера)))", re.IGNORECASE)
    re_name = re.compile(r"(?:меня)\s*(?:зовут)?\s*(\S*)\s*(?:зовут)?", re.IGNORECASE)
    re_company_name = re.compile(r"(?:(?:компания)\s*(\S*\s?бизнес))", re.IGNORECASE)
    
    
    data = pd.read_csv(csv)
    data_dict = {id: data[data['dlg_id'] == id] for id in data.dlg_id.unique()}
    statistics = dict(zip(data_dict.keys(),[None]*len(data_dict.keys())))
    
    for i in data_dict.keys():
        df_filtred = data_dict[i][data_dict[i]["role"] == "manager"][["line_n","text"]]
        greatings = df_filtred["text"].str.contains(re_greatings)
        farewells = df_filtred["text"].str.contains(re_farewells)
        name = df_filtred["text"].str.extract(re_name)
        company_name = df_filtred["text"].str.extract(re_company_name)
        statistics[i] = dict({"greatings" : greatings[greatings == True], "farewells" : farewells[farewells == True], \
            "name" : name[name[0].notna()], "company_name" : company_name[company_name[0].notna()] })
    
    for i in statistics:
        print("диалог: " + str(i))
        if statistics[i]['greatings'].empty:
            print(" Нет приветствия")
        else:
            print(" Приветствие на строчках: " + str([ i for i in statistics[i]['greatings'].index]))
        if statistics[i]['name'].empty:
            print(" Сотрудник не представился")
        else:
            print(" Сотрудника представился как: " + statistics[i]['name'].iloc[0].values[0])
        if statistics[i]['name'].empty:
            print(" Компания не упоминалась")
        else:
            print(" Была упомянута компания : " + statistics[i]['company_name'].iloc[0].values[0])
        if statistics[i]['farewells'].empty:
            print(" Нет прощания")
        else:
            print(" Прощание на строчках: " + str([ i for i in statistics[i]['farewells'].index]))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("test_data.csv")