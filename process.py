
#%%
import pandas as pd

#%%
data = pd.read_csv('computadores.csv').query('~processador.isna()')

data = (
    data
        .assign(
            ssd = data.ssd.astype(str),
            preco = data.preco.replace(
    {'[0-9]{2}x': '', 'sem juros no cartão': '', '^.*as ': '', '\s+de\s+': ' '},
    regex = True)
            .apply(lambda s: float(s.split()[0].replace('R$', '').replace('.', '').replace(',', '.'))),
            processador = data.processador.replace({'Processador ': ''}, regex = True)))

data = data.loc[["256" in val or "512" in val for val in data.ssd],:]

data = data.loc[['Core i' in f or 'Ryzen' in f for f in data.processador],:]

data = data[['processador', 'ssd', 'preco', 'link']]

# %%
data.to_csv('data.csv')
