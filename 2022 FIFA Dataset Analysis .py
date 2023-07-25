#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import library
import pandas as pd
import numpy as np
import os


# In[2]:


#set directory
os.chdir(r"C:\Users\Roswita Hede\Documents\Practice\Python\Data cleaning Fifa")


# In[3]:


df=pd.read_csv('fifa_data.csv')
df.head()


# In[4]:


df.info()


# # Data Cleaning
Based on the data above, tables that need to be cleaned are 
1. Team & contract
2. hits
3. joined
4. Height
5. value
6. Wage
7. position
# In[5]:


#Drop unecessary column
df_drop=['photoUrl','playerUrl','Loan Date End','Release Clause']
df=df.drop(columns=df_drop)


# In[6]:


#Clean the Team & Contract table
#Split team and contract into 2 columns
df['Team & Contract']=df['Team & Contract'].astype('str')
df['Team & Contract'].replace('\n', '', regex=True, inplace=True)
test=df['Team & Contract'][0]
Team=[]

Contract_Duration=[]
for i in range(len(df['Team & Contract'])):
    Team.append(str(df['Team & Contract'][i][:-11]))
    c=str(df['Team & Contract'][i][-11:])
    if c.startswith("2")==True:
        Contract_Duration.append(c)
    else:
        Contract_Duration.append("0")
df=df.drop(columns=['Team & Contract'])
df['Team']=Team
df['Contract_Duration']=Contract_Duration


# In[7]:


df.head()


# In[8]:


df['Hits'].isna().sum()


# In[9]:


#Clean Hits Column
import numpy as np

hits = []

for x in range(len(df["Hits"])):
    s = str(df["Hits"][x])
    s = s[1:].replace('K', '00')
    s = s.replace('/n', '')
    hits.append(s)

# Update the 'Hits' column with the new values
df['Hits'] = hits

# Convert the 'Hits' column to the desired data type, handling empty strings
df['Hits'] = pd.to_numeric(df['Hits'], errors='coerce').fillna(0).astype(int)


# In[10]:


df['Hits'].head()


# In[11]:


#Checking joined column
df['Joined'].head()


# In[12]:


#Changing the joined column into proper data time format
def month_to_number(x):
            if x== 'Jan':
                return 1
            elif x == 'Feb':
                return 2
            elif x == 'Mar': 
                return 3
            elif x == 'Apr':
                return 4
            elif x == 'May':
                return 5
            elif x == 'Jun': 
                return 6
            elif x == 'Jul': 
                return 7
            elif x == 'Aug': 
                return 8
            elif x == 'Sep': 
                return 9
            elif x == 'Oct': 
                return 10
            elif x == 'Nov':  
                return 11
            elif x == 'Dec':  
                return 12


# In[13]:


date = []
for x in range(len(df['Joined'])):
    d = df['Joined'][x]
    c = d.split(" ")
    month = str(month_to_number(c[0]))
    day = str(c[1].replace(',',''))
    year = str(c[2])
    if len(day) == 1:
        day = ('0'+str(day))
    date_long = (str(month)+'/'+str(day)+'/'+str(year))
    date_con = pd.to_datetime(date_long)
    date.append(date_con)


# In[14]:


df['Joined']=date
df['Joined'].head()


# In[15]:


#Change height into inches
temp_height=[]
for i in range(len(df['Height'])):
    i=df['Height'][i].replace('"','').split("'")
    inches=int(i[0])*12+int(i[1])
    temp_height.append(inches)
df['Height']=temp_height
df['Height'].head()


# In[16]:


#cleaning weight
temp_weight=[]
for x in range(len(df['Weight'])):
    temp_weight.append(int(df['Weight'][x].replace('lbs','')))
df['Weight']=temp_weight
df['Weight'].head()


# In[17]:


df['Value'].head()


# In[18]:


temp_value=[]
for i in range(len(df['Value'])):
    value = df['Value'][i]
    value = value.replace('€','')
    value = value.replace('K','000')
    value = value.replace('M','000000')
    value = value.replace('.','F')
    if 'F' in value:
        value = value.replace('F','')
        value = value=int(value)/10
    temp_value.append(int(value))
df['Value']=temp_value
df['Value'].head()


# In[19]:


temp_wage=[]
for i in range(len(df['Wage'])):
    Wage = df['Wage'][i]
    Wage = Wage.replace('€','')
    Wage = Wage.replace('K','000')
    Wage = Wage.replace('M','000000')
    Wage = Wage.replace('.','F')
    if 'F' in Wage:
        Wage = Wage.replace('F','')
        Wage = Wage=int(Wage)/10
    temp_wage.append(int(Wage))
df['Wage']=temp_wage
df['Wage'].head()


# In[20]:


df['SM'].head()


# In[21]:


df['W/F'].head()


# In[22]:


df['IR'].head()


# In[23]:


import re

# Remove non-digit characters from 'W/F' column
df['W/F'] = df['W/F'].apply(lambda x: re.sub(pattern="[^\d]", repl=" ", string=x))
df['SM'] = df['SM'].apply(lambda x: re.sub(pattern="[^\d]", repl=" ", string=x))
df['IR'] = df['IR'].apply(lambda x: re.sub(pattern="[^\d]", repl=" ", string=x))
df['W/F'].head()
df['SM'].head()
df['IR'].head()


# In[24]:


df['Positions'].unique()

There are many different positions, so we need to regroup the positions to reduce the size of group
# In[25]:


temp_position=[]
for x in range(len(df['Positions'])):
    y=sorted(df['Positions'][x].split(' '))
    yx=' '.join(y)
    temp_position.append(yx)
    
df['Positions']=temp_position
df['Positions']=df['Positions'].astype(object)
df['Positions'].unique()


# In[26]:


df = df.rename(columns={'Name': 'LongName', '↓OVA': 'Overall', 'POT': 'Potential', 'BOV': 'Best Overall', 'IR':'Reputation'})


# In[27]:


df.head()


# In[28]:


#download the clean data into csv
FIFA21_clean=df
FIFA21_clean.to_csv('cleaned_fifa21_dataset.csv', index=False)


# In[43]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[31]:


plt.figure(figsize=(10,12))
sns.heatmap(df.corr(numeric_only=True), vmin=0)
plt.show()


# Based on the heat map above, it can be seen that the goalkeer stats low correlation with value and wage of the  football player. The reason could be there are some other aspects to determine a value of goal keeper. Additionally, the variable height and weight have positive correlation to the goalkeeper stats, which means the higher the height, the better stats they are likely to have as goalkeeper.

# # Exploratory Data Analysis

# In[30]:


sns.jointplot(data=df, x='Age', y='Overall',hue='foot')


# Based on the scatter plot above, there is outlier in Age variables where the football player  is more than 50 years old. I decide to not drop this data point because it is possible to have an active player who are in his 50s.

# In[41]:


df.loc[df['Age']==53,['LongName','Nationality','Team']]


# In[57]:


sns.scatterplot(data=df, x='Value',y='Wage', hue='Value').set(title="Correlation of Value to Wage")


# Based on scatter plot above, it can be seen that there is a moderate positive correlation between Value and Wage, which indicate the higher the value could be a factor leads to higher wage However, there are 2 outlers, where one having higher value but lower wage, and the other have higher wage but lower value. let's find those two players

# In[50]:


df[df.Value>100000000].loc[:,['LongName','Nationality','Team','Overall','Value', 'Wage','Joined']]


# In[51]:


df[df.Wage>500000].loc[:,['LongName','Nationality','Team','Overall','Value', 'Wage','Joined']]


# In[58]:


sns.scatterplot(data=df, x='Overall',y='Wage', hue='Value').set(title="Correlation of Overall to Wage")


# For the overal less than 80, there seems lower correlation between overall and wage. However, it can be seen that for player with overall more than 80 points, have strong and positive impact to value and wage. because of that, I will look in more deeper to identify player having high overall rating but low market value and low wage.

# The tables below shows football players having high overall rating but low market value

# In[64]:


df[(df.Overall>85) & (df.Value<=20000000)].loc[:,['LongName','Nationality','Team','Overall','Value', 'Wage','Joined']].sort_values(by='Wage')


# The tables below shows football players having high overall rating but low wage

# In[65]:


df[(df.Overall>90) & (df.Wage<=300000)].loc[:,['LongName','Nationality','Team','Overall','Value', 'Wage','Joined']]\
.sort_values(by='Wage')


# In[37]:


plt.figure(figsize=(10,12))

#calculate the corelation between wage and the other numeric variables
correlation=df.corr(numeric_only=True)['Wage'].drop(['Value','Wage','GK Diving','GK Kicking','GK Reflexes',
                                                     'GK Positioning','Goalkeeping','GK Handling','Height','Weight'])
correlation = correlation.sort_values(ascending=False)
sns.barplot(x=correlation,y=correlation.index)
plt.title("Correlation of other parameters to Player's Wage")
plt.show()

It is showed from the bar graph above, Overal have is the most impactful parameter to a player's wage. It means that when the players have international reputation, the more famous a player is, the higher wage he likely to be offered.
# Below, shows the chart of top 10 player based on their overall performance

# In[68]:


top_ten_players = df.loc[:, ['LongName', 'Nationality', 'Team', 'Overall', 'Value', 'Wage', 'Joined']]\
                   .sort_values(by='Overall', ascending=False).head(10)
top_ten_players

