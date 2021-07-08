import pandas as pd
import matplotlib.pyplot as plt


'''OBTENER DATASET COMPLETO'''

df = pd.read_csv('https://raw.githubusercontent.com/alnunez/crypto_coins_historical_data/main/Binance_ADAUSDT_d.csv', skiprows=[0])

'''LIMPIAR DATOS'''


# Eliminar columnas irrelevantes
df.drop(['unix',	'symbol',	'high',	'low',	'Volume ADA',	'Volume USDT', 'tradecount'], axis=1, inplace=True)

# Restrigir datos a 365 días
df = df.head(365)

# Crear la columna delta
df.insert(3, 'delta', df['close']-df['open'])  

# Hallar % de variación diario
df.insert(2, '% var', (df['delta']/df['open'])*100)

# Convertir formato de date a tipo datetime
df['date'] = pd.to_datetime(df['date'])

# Convertir fecha a nombre del día de la semana
df['day'] = df['date'].dt.day_name()

# Filtrar variaciones negativas
df_neg = df[df['% var'] < 0]

# Agrupar por día, eliminar columnas irrelevantes, ordenar descendente.
df_count = df_neg.groupby('day').count()
df_count.drop(['date','delta','open','close'], axis=1, inplace=True)
df_count.sort_values('% var', ascending=False)
df_count.columns = ['count']


# Ordenar index por días de la semana
def sorter(column):
    order_day = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
    cat = pd.Categorical(column, categories=order_day, ordered=True)
    return pd.Series(cat)

df_count_sorted = df_count.sort_values(by="day", key=sorter)


'''GRAFICAR'''

df_count_sorted.rename(index={'Monday':'Mon', 'Tuesday':'Tue', 'Wednesday':'Wed','Thursday':'Thu','Friday':'Fri','Saturday':'Sat','Sunday':'Sun'}, inplace=True)

#Comparar cantidad de variaciones negativas en el año por día
plt.bar(df_count_sorted.index, df_count_sorted['count'], width=0.6, color=['r'])
plt.title('Number of time with negative price variation per week for ADA\n24/06/2020 to 25/06/2021')
plt.ylabel('Times')
plt.show()

# Variación en el tiempo  (negativa y positiva)
plt.figure(figsize=(10, 6))
plt.plot(df['date'],df['% var'])
plt.axhline(y=0, color='r')
plt.title('% Price Variation in ADA\nfrom 24/06/2020 to 25/06/2021\n')
plt.show()

# Variación en el tiempo (negativa)
df_neg.plot.line('date','% var', color='r', legend=False).set_title('% Negative Price Variation in ADA\nfrom 24/06/2020 to 25/06/2021\n')
plt.show()
