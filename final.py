from statistics import median_grouped
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')
st.title("The Nobel Prize ")
df_date = pd.read_csv('nobel_prizes_by_date.csv')
df_winner = pd.read_csv('nobel_prize_by_winner.csv')



#排序赋值
df_winner=df_winner.sort_values(by='id',ascending=True)
df_date=df_date.sort_values(by='id',ascending=True)
df_winner['date']=df_date['year']
df_winner.dropna(subset=['born','firstname'],inplace=True)
df_result= df_winner
df_result = df_result.drop(['index','died','bornCountryCode','bornCity','diedCountryCode','diedCity','share','overallMotivation','name','bornCountry','diedCountry'],axis=1)
df_result

#左边选择框
subject_filter = st.sidebar.multiselect(
     'choose the price type',
     df_winner.category.unique(),  # options
     df_winner.category.unique()) 
df_winner = df_winner[df_winner.category.isin(subject_filter)]
df_result = df_result[df_result.category.isin(subject_filter)]

#上方拉条
pop_filter = st.sidebar.slider('the year of getting the prize',1901,2016,1945)
df_winner = df_winner[df_winner['year'] <= pop_filter]
df_result = df_result[df_result['year'] <= pop_filter]

#显示国家
st.subheader('the country of the winner')
country = df_winner.country.value_counts()
fig ,ax=plt.subplots()
ax.set_xlabel('Countries',fontsize=10)
ax.set_ylabel('number of person/team',fontsize=10)
country.plot.bar()
st.pyplot(fig)

#问题分析
st.write('What is the relationship between people won the Nobel Prize and the level of development of country?')
st.write('As we can see from the graph, countries with higher levels of economic development have won more Nobel Prizes. For example, the United States, UK, which is inseparable from their strong comprehensive national power')

#显示学科
st.subheader('the subject of the winner')
fig, ax = plt.subplots()
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, 6))
category = df_winner.category.value_counts()
pie_result = df_winner.category.value_counts()
ax.pie(category, labels = pie_result.index, autopct='%3.1f%%',colors=colors, radius=3, center=(4, 4),       wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
st.pyplot(fig)

#显示年龄
st.subheader('the age of the getting award')
df_result['born'] = pd.to_datetime(df_result['born'])
df_result['birth_year'] = df_result.born.dt.year
df_result['awarded_at'] = df_result['year'] - df_result['birth_year']
fig ,ax=plt.subplots(1,2)
df_result.awarded_at.hist(ax=ax[0],bins=15)
ax[0].set_xlabel('age')
ax[0].set_ylabel('the numeber')
df_result.awarded_at.plot.box(ax=ax[1])
st.pyplot(fig)


#第二个问题分析
st.write('What is the relationship between people won the Nobel Prize and their age?')
st.write('We can see from these two figures, most of the people are between 45 and 65 years old to win the Nobel Prize, indicating that this is the best time for people to contribute to society')