import os
import re

import numpy as np
import pandas as pd
import pickle
import torch
from fuzzywuzzy import fuzz
from transformers import AutoTokenizer, AutoModel, logging


logging.set_verbosity_error()


class RecommendationModel:
    def __init__(self, product_data):
        self.product_data = pd.DataFrame(product_data)
        pickle_model_path = os.path.join(os.path.dirname(__file__), 'pickle_model_version_2.pkl')
        with open(pickle_model_path, "rb") as file:
            unpickler = pickle.Unpickler(file)
            self.pretrained_model = unpickler.load()
        self.tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
        self.model = AutoModel.from_pretrained("cointegrated/rubert-tiny")

    def preprocessing_bd(self):
        self.product_data.dropna(inplace=True)
        self.product_data['name'] = self.product_data['name'].apply(self.re_name)
        self.product_data['mera'] = self.product_data['name'].apply(self.add_metering)
        self.product_data['mera_let'] = self.product_data['mera'].apply(self.find_letters)
        self.product_data['mera_num'] = self.product_data['mera'].apply(self.find_numbers)

        self.product_data.drop(['mera'], axis=1, inplace=True)

        self.product_data.reset_index(drop=True, inplace=True)

        tokenized = self.product_data['name'].apply((lambda x: self.tokenizer.encode(x, add_special_tokens=True)))
        self.max_len = 0
        for i in tokenized.values:
            if len(i) > self.max_len:
                self.max_len = len(i)

        padded = np.array([i + [0] * (self.max_len - len(i)) for i in tokenized.values])
        attention_mask = np.where(padded != 0, 1, 0)
        input_ids = torch.tensor(padded)
        attention_mask = torch.tensor(attention_mask)
        with torch.no_grad():
            last_hidden_states = self.model(input_ids, attention_mask=attention_mask)
        self.product_name_vector = last_hidden_states[0][:, 0, :].numpy()  # вектор name производителя

    def result(self, parser_data, n_matchs=5):
        parser_data = pd.DataFrame(parser_data)
        parser_data['product_name'] = parser_data['product_name'].apply(self.re_name)

        parser_data['product_mera'] = parser_data['product_name'].apply(self.add_metering)
        parser_data['product_mera_let'] = parser_data['product_mera'].apply(self.find_letters)
        parser_data['product_mera_num'] = parser_data['product_mera'].apply(self.find_numbers)
        parser_data.drop(['product_mera'], axis=1, inplace=True)

        # -------Эмбеддинг для признака product_name-------
        tokenized = parser_data['product_name'].apply((lambda x: self.tokenizer.encode(x, add_special_tokens=True)))

        padded = np.array([i + [0] * (self.max_len - len(i)) for i in tokenized.values])
        attention_mask = np.where(padded != 0, 1, 0)
        input_ids = torch.tensor(padded)
        attention_mask = torch.tensor(attention_mask)

        with torch.no_grad():
            last_hidden_states = self.model(input_ids, attention_mask=attention_mask)
        product_dealer_name_vector = last_hidden_states[0][:, 0, :].numpy()

        # -------Скалярное произведение-------
        scalar = list()
        for i in range(self.product_name_vector.shape[0]):
            scalar.append(np.dot(self.product_name_vector[i], product_dealer_name_vector[0]))

        # -------Объединение таблиц-------
        df = pd.concat([self.product_data, parser_data.sample(self.product_data.shape[0], replace=True).reset_index(drop=True)], axis=1)
        df['scalar'] = pd.Series(scalar)
        df['product_mera_num'] = df['product_mera_num'].astype(float)
        df['mera_num'] = df['mera_num'].astype(float)

        to_kg = df.apply(lambda x: self.convert_to_kg(x['product_mera_let'], x['mera_let']), axis=1)
        to_g = df.apply(lambda x: self.convert_to_g(x['product_mera_let'], x['mera_let']), axis=1)

        df.loc[to_kg, 'product_mera_num'] /= 1000
        df.loc[to_g, 'product_mera_num'] *= 1000

        df['let'] = df['product_mera_let'] == df['mera_let']
        df.loc[to_kg, 'let'] = True
        df.loc[to_g, 'let'] = True
        df['let'] = df['let'].astype(int)

        id_df = df['id']

        # -------Добавление расстояние Левенштейна-------
        df['fuzz'] = df.apply(self.fuzzywuzzy_name, axis=1)

        df = df[['mera_num', 'product_mera_num', 'scalar', 'let', 'fuzz']]

        # -------Предсказания модели-------
        df['pred'] = self.pretrained_model.predict(df)
        df['product_id'] = id_df
        df = df.query('pred == 1').sort_values(['fuzz'], ascending=False)
        return df.product_id.to_list()[:n_matchs]

    # -------Функции предобработки-------
    def fuzzywuzzy_name(self, dataframe):
        """
        Добавление расстояния Левенштейна
        """
        return fuzz.token_set_ratio(dataframe['product_name'], dataframe['name'])

    def re_name(self, name):
        """
        Функция предобработки текста.
        Разделяет некоторые слитные слова.
        мылоPROSEPT -> мыло PROSEPT
        """
        return re.sub(r'(?<=[а-яa-z])(?=[A-Z])|(?=[а-я])(?<=[A-Za-z])|(?<=[a-z])(?=[0-9])', ' ', name)

    def add_metering(self, text):
        """
        Выделение метрики измерения и условным количеством из названия
        """
        try:
            return re.search(r'(\d{1,}(?:[\.,]\d+)?\s?(л|мл|кг|г))\b', text)[0]
        except Exception:
            return 0

    def find_letters(self, text):
        """
        Выделение метрики измерения после обработки текста функцией add_metering
        """
        try:
            return " ".join(re.findall(r'[A-Za-zА-Яа-я]+', text))
        except Exception:
            return "not"

    def find_numbers(self, text):
        """
        Выделение числа после обработки текста функцией add_metering
        """
        try:
            numbers = " ".join(re.findall(r'[-+]?(\d+[\.,]\d+|\d+)', text))
            return numbers.replace(",", ".")
        except Exception:
            return 0

    def convert_to_kg(self, product_mera_let, mera_let):
        """
        граммы в кг, мл в литры
        """
        return product_mera_let == 'г' and mera_let == 'кг' or product_mera_let == 'мл' and mera_let == 'л'

    def convert_to_g(self, product_mera_let, mera_let):
        """
        кг в граммы, литры в мл
        """
        return product_mera_let == 'кг' and mera_let == 'г' or product_mera_let == 'л' and mera_let == 'мл'
