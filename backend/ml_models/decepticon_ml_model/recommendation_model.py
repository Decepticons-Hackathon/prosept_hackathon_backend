
def recommendation_model(parser_data, product_data, n_matchs=5):
    """
    Функция с рекомендациями от модели
    Принимает на вход один товар дилера, бд от производителя и количество рекомендуемых товаров.
    Параметры:
    parser_data - [dict], key - product_name (название товара), dealer_id (id дилера);
    product_data - [dict], key - id (id товара), name (название товара), category_id (категория товара);
    n_matchs - int, количество рекомендаций.

    Возвращает список с id товарами производителя, в порядке убывания схожести.
    """
    import os
    import re

    import numpy as np
    import pandas as pd
    import pickle
    import torch

    from fuzzywuzzy import fuzz
    # from sklearn.metrics import precision_score
    from transformers import AutoTokenizer, AutoModel, logging

    logging.set_verbosity_error()

    # -------Функция предобработки текста-------
    def re_name(name):
        """
        Функция предобработки текста.
        Разделяет некоторые слитные слова.
        мылоPROSEPT -> мыло PROSEPT
        """
        return re.sub(
            r'(?<=[а-яa-z])(?=[A-Z])|(?=[а-я])(?<=[A-Za-z])|(?<=[a-z])(?=[0-9])',
            ' ',
            name
        )

    # -------Загрузка обученной модели для эмбеддинга-------
    tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
    model = AutoModel.from_pretrained("cointegrated/rubert-tiny")

    # -------Загружаем предобученную модель-------
    pickle_model_path = os.path.join(os.path.dirname(__file__), 'pickle_model.pkl')
    with open(pickle_model_path, "rb") as file:
        unpickler = pickle.Unpickler(file)
        pretrained_model = unpickler.load()

    # -------Предобработка данных-------
    parser_data = pd.DataFrame(parser_data)
    product_data = pd.DataFrame(product_data)

    product_data['category_id'].fillna(0, inplace=True)
    product_data.dropna(inplace=True)
    product_data['category_id'] = product_data['category_id'].astype(int)

    parser_data['product_name'] = parser_data['product_name'].apply(re_name)
    product_data['name'] = product_data['name'].apply(re_name)
    product_data.reset_index(drop=True, inplace=True)

    # -------Эмбеддинг для признака name-------
    tokenized = product_data['name'].apply(
        (lambda x: tokenizer.encode(x, add_special_tokens=True))
    )
    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)

    padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    product_name_vector = last_hidden_states[0][:, 0, :].numpy()

    # -------Эмбеддинг для признака product_name-------

    tokenized = parser_data['product_name'].apply(
        (lambda x: tokenizer.encode(x, add_special_tokens=True))
    )

    padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    product_dealer_name_vector = last_hidden_states[0][:, 0, :].numpy()

    # -------Скалярное произведение-------
    scalar = list()
    for i in range(product_name_vector.shape[0]):
        scalar.append(np.dot(product_name_vector[i], product_dealer_name_vector[0]))

    # -------Объединение таблиц-------
    df = product_data.copy()
    df['scalar'] = pd.Series(scalar)
    df['dealer_id'] = parser_data.loc[parser_data.index[0]].dealer_id
    df['product_name'] = parser_data.loc[parser_data.index[0]].product_name
    df = df.rename(columns={'id': 'product_id'})

    # -------Добавление расстояние Левенштейна-------
    def fuzzywuzzy_name(dataframe):
        return fuzz.token_set_ratio(dataframe['product_name'], dataframe['name'])

    df['fuzz'] = df.apply(fuzzywuzzy_name, axis=1)
    df.drop(['name', 'product_name'], axis=1, inplace=True)

    # -------Предсказания модели-------
    predictions = pd.DataFrame(pretrained_model.predict(df))

    df['pred'] = predictions

    df = df.query('pred == 1').sort_values(['fuzz'], ascending=False)

    return df.product_id.to_list()[:n_matchs]
