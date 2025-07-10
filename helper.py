import numpy as np
def get_medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally

def get_country_year_list(df):
    # Year list
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    # Country List
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

# writing function to fetch values when dropdown is selected based on year and country
def fetch_medal_tally(df,year,country):
  global temp_df
  medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  flag=0
  if year=='Overall' and country=='Overall':
    temp_df=medal_df
  if year=='Overall' and country!='Overall':
    flag=1
    temp_df=medal_df[medal_df['region']==country]
  if year!='Overall' and country=='Overall':
    temp_df=medal_df[medal_df['Year']==int(year)]
  if year!='Overall' and country!='Overall':
    temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]

  if flag==0:
    X=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
  else:
    X=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
  X['Total']=X['Gold']+X['Silver']+X['Bronze']
  return X

def data_over_time(df,col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nation_over_time.columns = ['Edition', col]
    nation_over_time = nation_over_time.sort_values('Edition')
    return nation_over_time

def yearwise_medal_tally(df,country):
    res_df = df.dropna(subset=['Medal'])
    res_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = res_df[res_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    res_df = df.dropna(subset=['Medal'])
    res_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = res_df[res_df['region'] == country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_country_wise(df,country):
  res_df=df.dropna(subset=['Medal'])
  res_df=res_df[res_df['region']==country]

  top_athletes = res_df['Name'].value_counts().reset_index().head(10)
  top_athletes.columns = ['Name', 'Medals']

  merged = top_athletes.merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']]
  merged = merged.drop_duplicates('Name')

  return merged

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final