## Анализ факторов, влияющих на продолжительность жизни в разных странах
  В ходе выполнения данного проекта будет сделано...
  Будут использованы...
  Цель: понять, какие экономические, социальные и экологические факторы наиболее сильно влияют на среднюю продолжительность жизни. 
### Шаг 1. Подготовка к работе, импорт необходимых библиотек
Импортируем необходимые библиотеки: pandas(для импорта csv-файлов и обработки DataFrame), matplotlib.pyplot(для построения графиков), numpy(для выборки большого количества данных и работы с ними, чтобы не использовать циклы и списки; это позволит сократить время работы программы и количество используемой памяти), seaborn(также для визуализации).
```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
```

### Шаг 2. Импорт данных.
Основным нашим файлом будет csv с данными о средней продолжительности жизни по странам и регионам. Также для выявления корреляций будут использованы файлы, содержащие информацию об инвестициях государства на здравоохранение, уровнем образования и ВВП на душу населения.
```python
df = pd.read_csv(r'Pet-Project\people.csv', on_bad_lines='skip')
vvp = pd.read_csv(r'Pet-Project\vvp.per.pers.csv', on_bad_lines='skip')
health = pd.read_csv(r'Pet-Project\zdravoohr.csv', on_bad_lines='skip')
gra = pd.read_csv(r'Pet-Project\gramotn.csv', on_bad_lines='skip')
```

### Шаг 3. Очистка данных(пустых ячеек, пустых значений, неправильных данных(выбросов))


```python
for i in df.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        fill = df[i].mean()
        df.fillna({i: fill}, inplace=True)
```


```python
for i in df.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        df[i] = np.where(df[i] < 30, 30, df[i])
```

### Шаг 4. Выявление интересующих данных + построение графиков.
№1. Как распределена продолжительность жизни по странам? Мы берём частоту разных величин продолжительности жизни
```python
df['2023'].plot(kind='hist', color='#CD5C5C')
plt.xlabel('average-life-expectancy')
plt.show()
```
На выходе получаем следующий график:

<img width="389" height="262" alt="image" src="https://github.com/user-attachments/assets/56a0541d-d84c-490c-8adf-45d7c6f1f235" />
Можно сделать вывод, что примерно в половине стран люди в среднем живут от 70 до 78. Если смотреть более обобщённо, то от 60 до 85. Остальные немного меньшо, но встречается это гараздо реже.

№2. Какие 10 стран имеют самую высокую и низкую продолжительность жизни?
```python
new = df[['Country Name', '2022']]
asc = new.sort_values('2022', ascending=True)
desc = new.sort_values('2022', ascending=False)
print('5 стран с самой низкой продолжительностью жизни')
print(asc[0:5])
print('5 стран с самой высокой продолжительностью жизни')
print(desc[0:5])

plt.subplot(2, 1, 1)
plt.barh(asc['Country Name'][0:5], asc['2022'][0:5], color='hotpink')

plt.subplot(2, 1, 2)
plt.barh(desc['Country Name'][0:5], desc['2022'][0:5], color='purple')
```
На выходе получим следующий график:
<img width="476" height="248" alt="image" src="https://github.com/user-attachments/assets/5e7cb403-a6fe-4004-98e0-32df8574c8a6" />

№3. Как изменилась средняя продолжительность жизни в мире с 2000 по 2015 год?
```python
x = df['2000'].mean()
print(x)
y = df['2015'].mean()
print(y)

print(f'Средняя продолжительнось жизни \
изменилась на {round(y - x, 3)} лет.')
res = round(y - x, 3)
years = ['2000', '2001', '2002', '2003', '2004',
         '2005', '2006', '2007', '2008', '2009',
         '2010', '2011', '2012', '2013', '2014', '2015']
li = []
for i in df.columns:
    if i in years:
        li.append(df[i].mean())
        
plt.plot(years, li, marker = 'o', color='purple', label='Мир в среднем')

ru = []
country_name = 'Russian Federation'
country_data = df[df['Country Name'] == country_name]
for i in country_data.columns:
    if i in years:
        ru.append(country_data[i].values[0])
plt.plot(years, ru, marker = 'o', color='hotpink', label='Российская Федерация')
plt.title('Динамика продолжительности жизни: Россия vs Мир (2000–2015)')
plt.xlabel('Год')
plt.ylabel('Продолжительность жизни (лет)')
plt.legend() # начнут отображаться метки мир и рф
plt.xticks(rotation=45) # подписи годов под углом 45
plt.tight_layout() # пошире стал график
```
На выходе получаем:

<img width="447" height="280" alt="image" src="https://github.com/user-attachments/assets/31dc03a8-deb4-4f42-8bef-ced85d05c467" />

```python

```

```python

```

```python

```

```python

```

```python

```







