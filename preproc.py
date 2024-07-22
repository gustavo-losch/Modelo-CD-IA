# -*- coding: utf-8 -*-
from copy import copy
import pandas as pd
import numpy as np
from itertools import chain

#carregando arquivo
df = pd.read_csv('steam-games.csv')
df.head()
print(f"columns: {len(df.columns)}")
print(f"rows: {len(df)}")

#ajustando valores nulos
df['genres'] = df['genres'].fillna('')
df['categories'] = df['categories'].fillna('')
df = df[df['genres'].notnull() & df['categories'].notnull()]

#criando as colunas para categorias e generos
df['categories'] = df['categories'].apply(lambda x: x.replace(', ', ',').split(','))
df['genres'] = df['genres'].apply(lambda x: x.replace(', ', ',').split(','))
category_columns = set(chain.from_iterable(list(df['categories'].values)))
print(f"number of categories: {len(category_columns)}")
genre_columns = set(chain.from_iterable(list(df['genres'].values)))
print(f"number of genres: {len(genre_columns)}")
category_dict = { cat: np.zeros(42497) for cat in category_columns }
genre_dict = { cat: np.zeros(42497) for cat in genre_columns }

#atribuindo 0 ou 1 para as instancias do dataset
for i, row in df.iterrows():
    for cat in row['categories']:
      if cat in category_dict:
        category_dict[cat][i] = 1.0
    for genre in row['genres']:
      if genre in genre_dict:
        genre_dict[genre][i] = 1.0

#oragizando a nomenclatura das colunas de saida
lower_category_dict = {k.lower().replace(' ', '_'): v for k,v in category_dict.items()}
lower_category_dict['null_category'] = lower_category_dict.pop('')
lower_genre_dict = {k.lower().replace(' ', '_'): v for k,v in genre_dict.items()}
lower_genre_dict['null_genre'] = lower_genre_dict.pop('')

#criando colunas de genero e categoria
category_df = pd.DataFrame(lower_category_dict)
genre_df = pd.DataFrame(lower_genre_dict)
category_genre_df = pd.concat([category_df, genre_df], axis=1)

# validando se o join ocorreu com sucesso
category_genre_df[category_genre_df.isnull().any(axis=1)]

#resultado
result = pd.concat([df, category_genre_df], axis=1)

#validações
pd.set_option('display.max_columns', None)
len(result.columns)
new_cols = list(set(list(lower_category_dict.keys()) + list(lower_genre_dict.keys())))
new_cols.sort()
old_cols = list(set(set(result.columns) - set(new_cols)))
old_cols.sort()
check_new_col_df = result[new_cols]
check_new_col_df[check_new_col_df.isnull().any(axis=1)]
result[['genres', 'categories'] + new_cols]
result[old_cols + new_cols]

#salvando
result[old_cols + new_cols].to_csv('steam_games_preproc.csv', index=False)