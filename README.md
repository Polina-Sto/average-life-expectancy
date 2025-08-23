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

