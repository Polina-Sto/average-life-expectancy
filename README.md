# Анализ факторов, влияющих на продолжительность жизни в разных странах
  В ходе выполнения данного проекта будет проведён анализ продолжительности жизни по различным странам и годам, чистка данных и поиск выбросов, выявление корреляций с уровнем ВВП на душу населения, инвестициями в здравоохранение и уровнем образования. <br />
  Будут использованы: язык программирования Python, библиотеки Pandas, Numpy, matplotlib, seaborn. <br />
  Цель: понять, какие экономические и социальные факторы наиболее сильно влияют на среднюю продолжительность жизни. 
## Шаг 1. Подготовка к работе, импорт необходимых библиотек
Импортируем необходимые библиотеки: pandas(для импорта csv-файлов и обработки DataFrame), matplotlib.pyplot(для построения графиков), numpy(для выборки большого количества данных и работы с ними, чтобы не использовать циклы и списки; это позволит сократить время работы программы и количество используемой памяти), seaborn(также для визуализации).
```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
```

## Шаг 2. Импорт данных.
Основным нашим файлом будет csv с данными о средней продолжительности жизни по странам и регионам. Также для выявления корреляций будут использованы файлы, содержащие информацию об инвестициях государства на здравоохранение, уровнем образования и ВВП на душу населения. Файлы скачаны с официального сайта "World Bank Open Data".  <br />
Название папки проекта на локальном компьютере - Pet-Project, поэтому указываем соответствующий путь:
```python
df = pd.read_csv(r'Pet-Project\people.csv', on_bad_lines='skip')
vvp = pd.read_csv(r'Pet-Project\vvp.per.pers.csv', on_bad_lines='skip')
health = pd.read_csv(r'Pet-Project\zdravoohr.csv', on_bad_lines='skip')
gra = pd.read_csv(r'Pet-Project\gramotn.csv', on_bad_lines='skip')
```

## Шаг 3. Очистка данных(пустых ячеек, пустых значений)

Пройдёмся циклом по колонкам DataFrame, минуя существующие колонки с текстовыми значениями. После этого заполним пропуски и пустые значения средним значением по миру.  <br />
```python
for i in df.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        fill = df[i].mean()
        df.fillna({i: fill}, inplace=True)
```

## Шаг 4. Выявление интересующих данных + построение графиков.
### №1. Как распределена продолжительность жизни по странам? 
Мы берём частоту разных величин продолжительности жизни.
```python
df['2023'].plot(kind='hist', color='#CD5C5C')
plt.xlabel('average-life-expectancy')
plt.show()
```
На выходе получаем следующий график: <br />

<img width="382" height="262" alt="image" src="https://github.com/user-attachments/assets/95feceec-8366-4466-9420-004253a0fe90" />

Можно сделать вывод, что примерно в половине стран люди в среднем живут от 70 до 85. Если смотреть более обобщённо, то от 60 до 87. Остальные немного меньшо, но встречается это гараздо реже.

### №2. Какие 10 стран имеют самую высокую и низкую продолжительность жизни?
Создадим новый DataFrame с значениями только за конкретный год и названием страны. Производим сортировку по возрастанию и по убыванию, выбодим топ 5 стран. Строим 2 графика.
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
На выходе получим следующий график: <br />

<img width="476" height="248" alt="image" src="https://github.com/user-attachments/assets/5e7cb403-a6fe-4004-98e0-32df8574c8a6" />

### №3. Как изменилась средняя продолжительность жизни в мире с 2000 по 2015 год?
Поиск среднего значения по определённому году(т.е. по столбцу). Посчитаем и выведем на сколько изменилась средняя продолжительности жизни.
```python
x = df['2000'].mean()
print(x)
y = df['2015'].mean()
print(y)

print(f'Средняя продолжительнось жизни \
изменилась на {round(y - x, 3)} лет.')
res = round(y - x, 3)
```
Для построения более детального графика нам необходимо найти данные по каждому году, затем на их основе построить график, отражающий динамику. Создадим цикл, который будет искать и добавлять в список данные по каждому году. После этого строим график. При желании можно найти данные по определённой стране и также добавить на график.
```python
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

<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/31dc03a8-deb4-4f42-8bef-ced85d05c467" />


### №4. Есть ли выбросы в наборе данных?
То есть мы постараемся найти все значения, которые сильно отличаются от остальных. Например, средняя продолжительность жизни составляет 12 лет, Такого явно мне может быть в рамках целой страны. Будем считать, что это значение не может составлять менее 27 лет в рамках одной страны. Заменим все значения в массиве менее 27.
```python
for i in df.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        df[i] = np.where(df[i] < 27, 27, df[i])
        # or 
        # df[data_cols] = df[data_cols].mask(df[data_cols] < 27, 27)
        
        sns.boxplot(data=df, x=i)
        plt.show()
```
Если интересно узнать какие именно значения являются выбросами, то напишем:
```python
for i in df.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        for i in df[i]:
            if i < 27:
                print(i)
```
и получим следующий рез-т: <br />
25.633 25.858 26.103 25.396 25.632 26.522 25.777 12.784 24.314 11.632 25.863 11.295 24.875 11.573 22.933 24.172 20.721 10.989 25.418 25.034 21.938 22.263 12.158 19.048 14.665 18.818 <br />
Это значение из всего массива данных. Возможно, что значения близкие к 30 могли быть в малоразвитых странах. Но средняя продолжительность жизни 10 лет точно не могла существовать.

## Шаг 5. Выявление корреляций с экономическими и социальными факторами.
Очистим данные также, как мы делали раньше, в других DF. Проверим формат данных, заменим пустые значения на медиану в рамках страны(т.е. строки, axis=1).
```python
year_columns = [col for col in vvp.columns if col.isdigit()]
vvp['median_gdp_by_years'] = vvp[year_columns].median(axis=1)
for i in vvp.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        vvp.fillna({i: vvp['median_gdp_by_years']}, inplace=True)
```
Выеберем данные только за определённый год. В нашем случае 2023. Сделаем объёдинение таблиц.
```python
year = '2023'
# Функция для извлечения данных по году
def extract_year_data(df, indicator_name):
    df_clean = df[['Country Name', 'Country Code', year]].copy()
    df_clean = df_clean.rename(columns={year: indicator_name})
    df_clean[indicator_name] = pd.to_numeric(df_clean[indicator_name], errors='coerce')
    return df_clean[['Country Name', 'Country Code', indicator_name]]

df = extract_year_data(df, 'life_expectancy')
vvp = extract_year_data(vvp, 'gdp_per_capita')
health = extract_year_data(health, 'health_spending')
gra = extract_year_data(gra, 'smart')

df_final = df
for df in [vvp, health, gra]:
    df_final = df_final.merge(df, on=['Country Name', 'Country Code'], how='outer')

df_final = df_final.drop('Country Code', axis=1)
```
Проведём корреляцию и построим "тепловую карту" со значениями.
```python
corr = df_final.select_dtypes(include=[float, int]).corr()
print("Корреляция с продолжительностью жизни:")
print(corr)

sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Корреляция показателей')
plt.show()
```

Корреляция признаков по 2021 году: <br />
<img width="500" height="380" alt="image" src="https://github.com/user-attachments/assets/b2ffcfa7-8c9b-4d4b-b9f9-cc468662c24d" />  <br />
Как можно увидеть на графике, в 2021 годе наибольшая корреляция есть у средней продолжительности жизни и уровнем образования, составляет 0.8. То есть при росте образования с вероятностью 80% растёт средняя продолжительности жизни. Также показатель зависит от ВВП на душу населения на 65% - это является средним показателем корреляции.

Корреляция по 2023 году: <br />
<img width="500" height="380" alt="image" src="https://github.com/user-attachments/assets/0cbac562-218c-4b12-88fd-df6ee1d0fa7a" /> <br />
Однако в 2023 году происходит немного другое. Здесь также можно наблюдать корреляцию между продолжительностью жизни и уровнем образования 0.91, с ВВП - 62%. Но также за 2023 год данные показывают, что показатель коррелирует с уровнем инвестиций в здравоохранение на 71%, что также является значительным.

## Выводы
&#x1F493
```python

```




