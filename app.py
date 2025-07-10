import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor,helper
import plotly.figure_factory as ff
import plotly.express as px

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympic Analysis ')

user_menu=st.sidebar.radio(
'Select an option',
('Medal Tally','Overall Analysis', 'Country-wise Analysis','Athlete-wise Analysis'),)

if user_menu== 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.get_country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+' Overall Tally')
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally in '+str(selected_year)+' Olympics')
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country+' performance in '+str(selected_year)+' Olympics')
    st.dataframe(medal_tally)

# Getting stats of some data

if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    nations_over_time=helper.data_over_time(df,'region')
    fig, ax = plt.subplots()
    ax.plot(nations_over_time['Edition'], nations_over_time['region'])

    ax.set_xlabel('Edition')
    ax.set_ylabel('No of Countries')
    ax.set_title('Number of Participating Nations Over Year')

    st.pyplot(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig, ax = plt.subplots()
    ax.plot(events_over_time['Edition'], events_over_time['Event'])

    ax.set_xlabel('Edition')
    ax.set_ylabel('Events')
    ax.set_title('Number of Events Over Year')

    st.pyplot(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig, ax = plt.subplots()
    ax.plot(athletes_over_time['Edition'], athletes_over_time['Name'])

    ax.set_xlabel('Edition')
    ax.set_ylabel('Name')
    ax.set_title('Number of Athletes Over Year')

    st.pyplot(fig)

    st.title('No of Events Over time(Every Sport)')
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Tally')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select Country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig, ax = plt.subplots()
    ax.plot(country_df['Year'], country_df['Medal'])

    ax.set_xlabel('Year')
    ax.set_ylabel('Medal')
    ax.set_title('Medal Tally Over Year')

    st.pyplot(fig)

    st.title(selected_country+' excels in following sports')
    pt=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    top10_df=helper.most_successful_country_wise(df,selected_country)
    st.title('Top 10 athletes of '+selected_country)
    st.table(top10_df)

if user_menu=='Athlete-wise Analysis':
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig=ff.create_distplot([x1,x2,x3,x4],['Age','Gold Medal','Silver Medal','Bronze Medal'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)