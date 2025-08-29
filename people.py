import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression


df = pd.read_csv(r'Pet-Project\people.csv', on_bad_lines='skip')
vvp = pd.read_csv(r'Pet-Project\vvp.per.pers.csv', on_bad_lines='skip')
health = pd.read_csv(r'Pet-Project\zdravoohr.csv', on_bad_lines='skip')
gra = pd.read_csv(r'Pet-Project\gramotn.csv', on_bad_lines='skip')



for i in df.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        fill = df[i].mean()
        df.fillna({i: fill}, inplace=True)
   
        
df['2023'].plot(kind='hist', color='#CD5C5C')
plt.xlabel('Распределение средней продолжительности жизни в 2023 году')
plt.ylabel('Частота')
plt.show()


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
plt.xlabel('''Страны с самой низкой(сверху) и 
            самой высокой(снизу продолжительностью жизни''')
plt.show()

x = df['2000'].mean()
print(x)
y = df['2015'].mean()
print(y)
print(f'Средняя продолжительность жизни \
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
plt.show()

for i in df.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        df[i] = np.where(df[i] < 27, 27, df[i])
        
        
year_columns = [col for col in vvp.columns if col.isdigit()]
vvp['median_gdp_by_years'] = vvp[year_columns].median(axis=1)
for i in vvp.columns:
    if i in ['Country Name', 'Country Code', 
               'Indicator Name', 'Indicator Code', 'Unnamed: 69']:
        continue
    else:
        vvp.fillna({i: vvp['median_gdp_by_years']}, inplace=True)
        
        
year = '2021'
# Функция для извлечения данных по году
def extract_year_data(df, indicator_name):
    df_clean = df[['Country Name', 'Country Code', year]].copy()
    df_clean = df_clean.rename(columns={year: indicator_name})
    df_clean[indicator_name] = pd.to_numeric(df_clean[indicator_name], errors='coerce')
    return df_clean[['Country Name', 'Country Code', indicator_name]]

df = extract_year_data(df, 'life_expectancy')
vvp = extract_year_data(vvp, 'gdp_per_capita')
health = extract_year_data(health, 'health_spending')
gra = extract_year_data(gra, 'education')

df_final = df
for df in [vvp, health, gra]:
    df_final = df_final.merge(df, on=['Country Name', 'Country Code'], how='outer')

df_final = df_final.drop('Country Code', axis=1)

for i in df_final.columns:
    if i == 'Country Name':
        continue
    else:
        fill = df_final[i].median()
        df_final.fillna({i: fill}, inplace=True)


print(df_final.head(10).to_string())

corr = df_final.select_dtypes(include=[float, int]).corr()
print("Корреляция с продолжительностью жизни:")
print(corr)

sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title(f'Корреляция показателей в {year} году')
plt.xticks(rotation=45) 
plt.tight_layout() 
plt.show()


x = df_final[['gdp_per_capita', 'health_spending', 'education']]
y = df_final['life_expectancy']   

model = LinearRegression()
model.fit(x, y)

years = model.predict([[30000, 4, 50]])
print(years)
