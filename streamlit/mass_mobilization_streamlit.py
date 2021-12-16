import streamlit as st
import requests

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

from PIL import Image
from io import BytesIO
import re
import mass_mobil_functions as mmf

import joblib

#World Governance Indicators, to look at change in indicators over time
wgi = pd.read_csv('../data/transformed/wgi_pivot.csv')

#import cleaned FIW data
fiw = pd.read_csv('../data/transformed/fiw_clean.csv')

#fully cleaned and merged df for general exploration
df = pd.read_csv('../data/transformed/mm_wgi_fiw.csv')

#importing cleaned mm data
mm = pd.read_csv('../data/transformed/mass_mobilization_data_cleaned.csv')

#silence deprecationwarnings
st.set_option('deprecation.showPyplotGlobalUse', False)


#setting a seaborn color
# colors = "CMRmap_r"
sns.set_palette("icefire")

country_list = sorted(['Canada', 'Cuba', 'Haiti', 'Dominican Republic (the)', 'Jamaica',
       'Mexico', 'Guatemala', 'Honduras', 'El Salvador', 'Nicaragua',
       'Costa Rica', 'Panama', 'Colombia',
       'Venezuela (Bolivarian Republic of)', 'Guyana', 'Suriname',
       'Ecuador', 'Peru', 'Brazil', 'Bolivia (Plurinational State of)',
       'Paraguay', 'Chile', 'Argentina', 'Uruguay',
       'United Kingdom of Great Britain and Northern Ireland (the)',
       'Ireland', 'Netherlands (the)', 'Belgium', 'France', 'Switzerland',
       'Spain', 'Portugal', 'Germany', 'Poland', 'Austria', 'Hungary',
       'Czech Republic (the)', 'Slovakia', 'Italy', 'Albania', 'Kosovo',
       'Serbia', 'the former Yugoslav Republic of Macedonia', 'Croatia',
       'Bosnia and Herzegovina', 'Montenegro', 'Slovenia', 'Greece',
       'Cyprus', 'Bulgaria', 'Republic of Moldova (the)', 'Romania',
       'Russian Federation (the)', 'Estonia', 'Latvia', 'Lithuania',
       'Ukraine', 'Belarus', 'Armenia', 'Georgia', 'Azerbaijan',
       'Finland', 'Sweden', 'Norway', 'Denmark', 'Guinea-Bissau',
       'Equatorial Guinea', 'Gambia (the)', 'Mali', 'Senegal', 'Benin',
       'Mauritania', 'Niger (the)', "Côte d'Ivoire", 'Guinea',
       'Burkina Faso', 'Liberia', 'Sierra Leone', 'Ghana', 'Togo',
       'Cameroon', 'Nigeria', 'Gabon', 'Central African Republic (the)',
       'Chad', 'Congo (the)', 'Democratic Republic of the Congo (the)',
       'Uganda', 'Kenya', 'United Republic of Tanzania (the)', 'Burundi',
       'Rwanda', 'Somalia', 'Djibouti', 'South Sudan', 'Ethiopia',
       'Eritrea', 'Angola', 'Mozambique', 'Zambia', 'Zimbabwe', 'Malawi',
       'South Africa', 'Namibia', 'Lesotho', 'Botswana', 'Madagascar',
       'Comoros (the)', 'Mauritius', 'Morocco', 'Algeria', 'Tunisia',
       'Libya', 'Sudan (the)', 'Iran (Islamic Republic of)', 'Turkey',
       'Iraq', 'Egypt', 'Syrian Arab Republic', 'Lebanon', 'Jordan',
       'Saudi Arabia', 'Yemen', 'Kuwait', 'Bahrain',
       'United Arab Emirates (the)', 'Oman', 'Afghanistan',
       'Turkmenistan', 'Tajikistan', 'Kyrgyzstan', 'Uzbekistan',
       'Kazakhstan', 'China', 'Mongolia', 'Taiwan',
       "Democratic People's Republic of Korea (the)",
       'Republic of Korea (the)', 'Japan', 'India', 'Pakistan',
       'Bangladesh', 'Myanmar', 'Sri Lanka', 'Nepal', 'Thailand',
       'Cambodia', 'Viet Nam', 'Malaysia', 'Singapore',
       'Philippines (the)', 'Indonesia', 'Timor-Leste',
       'Papua New Guinea'])


st.sidebar.title('Mass Mobilization and World Changing')
st.sidebar.subheader('A Study of the Mass Mobilization Dataset Alongside Various Indices')



page = st.sidebar.selectbox( 'Select a page', ('About', 'Data by Country', 'Case Studies', 'Multiclass Classification Model'))

if page == 'About':
    st.header('Mass Mobilization and World Changing')
    st.subheader('A Study of the Mass Mobilization Dataset Alongside Various Indices')


    # git, slides = st.columns(2)
    # git.success('Project GitHub Source')
    # git.markdown("[![Foo](https://img.icons8.com/material-outlined/96/000000/github.png)](https://github.com/tjohn07/mass_mobilization_and_world_changing)")
    # slides.success('Project Slides')
    # slides.markdown("[![Foo](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Google_Slides_logo_%282014-2020%29.svg/72px-Google_Slides_logo_%282014-2020%29.svg.png)](https://docs.google.com/presentation/d/1tLYIMdbjOniqPUQpQOYjEvaOj-24g1e41QbFLGiLISc/edit#slide=id.p)")

    #inspired by this personal website : https://github.com/v4gadkari/vgpersonalwebsite/blob/main/streamlit_app.py
    st.sidebar.info('Terri John')
    cols1, cols2 = st.sidebar.columns(2)
    cols1.markdown("[![Foo](https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-48.png)](https://www.linkedin.com/in/terri-john/)")
    cols2.markdown("[![Foo](https://img.icons8.com/material-outlined/48/000000/github.png)](https://github.com/tjohn07)")

if page == 'Data by Country':

    st.header('Metrics by Country and Year')
    with st.expander("A description of the metrics:"):
         st.markdown('##### Control of Corruption: Estimate (CC.EST):')
         st.write('* Control of Corruption captures perceptions of the extent to which public power is exercised for private gain')
         st.write('')
         st.markdown('##### Government Effectiveness: Estimate (GE.EST):')
         st.write('* Government Effectiveness captures perceptions of the quality of public service')
         st.write('')
         st.markdown('##### Political Stability and Absence of Violence/Terrorism: Estimate (PV.EST):')
         st.write('* Political Stability and Absence of Violence/Terrorism measures perceptions of the likelihood of political instability and/or politically-motivated violence')
         st.write('')
         st.markdown('##### Rule of Law: Estimate:')
         st.write('* Rule of Law captures perceptions of the extent to which agents have confidence in and abide by the rules of society')
         st.write('')
         st.markdown('##### Voice and Accountability: Estimate:')
         st.write('* Voice and Accountability captures perceptions of the extent to which a country\'s citizens are able to participate in selecting their government')
         st.write('')
         st.markdown('##### Number of Protests:')
         st.write('* Protest count in the given year.')
         st.write('')
         st.markdown('##### Freedom in the World Score (FIW):')
         st.write('* "Freedom House rates people’s access to political rights and civil liberties in 210 countries and territories through its annual Freedom in the World report."')
         st.write(' - Scores are in 3 tiers: Not Free: 0, Partially Free: 1, Free: 2')


    country = st.text_input("Enter a Country Name", 'Tunisia')


    def time_series_by_country(df=wgi, df2=fiw, df3 = mm, country=None, cols=['CC.EST', 'GE.EST', 'PV.NO.SRC', 'RL.EST', 'VA.EST'],
                               cols2=['fiw_status'], cols3=['protest'],title='Title', xlab='Year', ylab='Metric Score / Protest Count', steps=1):

            '''
            A function to plot WGI, protest count, and FIW score by year.
            input: a cleaned worldbank dataframe and a country
            output: a country specific dataframe with a datetime index by year and plot it
            '''

            #filter wgi dataframe by country and plot
            df = df[df['country_name'] ==  country.title()]
            #sort by year
            df = df.sort_values(by='year')
            #set index to datetime object by year
            df.index = pd.to_datetime(df['year'], format='%Y').dt.year
            #return datetime index dataframe for specified country


            #filter fiw dataframe by country and plot
            le = LabelEncoder()
            df2['fiw_status'] = le.fit_transform(df2['fiw_status'])
            df2 = df2[df2['country_name'] ==  country.title()]
            #sort by year
            df2 = df2.sort_values(by='year')
            #set index to datetime object by year
            df2.index = pd.to_datetime(df2['year'], format='%Y').dt.year
            #return datetime index dataframe for specified country

            #clean and filter mm dataframe by country/date and plot
            cols_to_drop = df3.drop(columns = ['country_name', 'year', 'region', 'protest', 'duration_int', 'region']).columns
            df3 = df3.drop(cols_to_drop, axis=1)
            df3 = df3[df3['country_name'] == country.title()]
            df3 = pd.DataFrame(df3.groupby(df3['year'])['protest'].sum())
            df3.index = pd.to_datetime(df3.index, format='%Y').year

            plt.figure(figsize=(25,14))

            # Iterate through each column name.
            for col in cols:

                # Generate a line plot of the column name.
                # You only have to specify Y, since our
                # index will be a datetime index.
                plt.plot(df[col], label=col)

            for col2 in cols2:

                # Generate a line plot of the column name.
                # You only have to specify Y, since our
                # index will be a datetime index.
                plt.plot(df2[col2], label=col2, marker='o')

            for col3 in cols3:

                # Generate a line plot of the column name.
                # You only have to specify Y, since our
                # index will be a datetime index.
                plt.plot(df3[col3], label=col3, marker='^')



            # Generate title and labels.
            plt.title(f'World Governance Indicators, Freedom Score, and Protest Count from 1996-2021: {country.title()}', fontsize=26)
            plt.xlabel(xlab, fontsize=20)
            plt.ylabel(ylab, fontsize=20)
            plt.legend()

            # Enlarge tick marks.
            plt.yticks(fontsize=18)
            plt.xticks(df.index[0::steps], fontsize=12, rotation=20);


    st.pyplot(time_series_by_country(wgi, fiw, mm, country=country))







if page == 'Case Studies':
    st.title('Tunisia: A Case Study')
    st.write('------------------------------------')
    container = st.container()
    # with st.container():
    container.image('./streamlit_images/tunisia_metrics.png')
    st.write('During the EDA phase of this project, I checked to see how many countries had moved around on the Freedom House scale.  In looking specifically at the top 60 countries for frequency in the Mass Mobilization dataset, I found that only 2 countries had transitioned through all three scores, from ‘Not Free’ to ‘Partially Free’ to ‘Free.’')
    st.write('')
    st.write('Here we can take a closer look at Tunisia’s metrics over the years. Tunisia was ranked as ‘Partially Free’ from 2006-2011, when it then transitioned to ‘Free,’ where it remained through 2014. This is the period following the ‘Arab Spring.’ ')
    st.write('')
    st.write('In 2015 we see a dip in the number of protests corresponding to the drop to ‘Not Free,’ where Tunisia has remained ranked to the present day. We see a spike in the number of protests in 2018, 3 years after the change in rank to ‘Not Free,’ which are noted as pertaining to cost of living and taxes. ')
    st.write('')
    st.caption('Source: https://en.wikipedia.org/wiki/2018_Tunisian_protests')

    st.write('------------------------------------')
    st.title('Mali: A Case Study')
    st.write('------------------------------------')
    container = st.container()
    # with st.container():
    container.image('./streamlit_images/mali_metrics.png')
    st.write("In taking a closer look at Mali, we see that it was ranked 'Not Free' until 2012, was upgraded to 'Partially Free' in 2013, and then to 'Free' from 2014-2020. In 2012, just preceding the change to 'Partially Free,' we can not a spoke in number or protests. It doing some light research, we see that Mali experienced a coup in 2012. You can read more about the situation in Mali here:")
    st.caption('https://freedomhouse.org/country/mali/freedom-world/2021. ')

# Content Based Filtering

if page == "Multiclass Classification Model":

    # load the multiclass classification model
    stacks = joblib.load('./models/multiclass.pkl')

    # @st.cache()

    st.header('Predicting State Response to a Protest')


    def prediction(country, year, protester_violence, participants_count, duration,
                   motivation):

        """
        A function to generate predictions of state response using a stacked multiclass classification model
        """

        get_country_stats_mm = mm[(mm['country_name'] == country) ].reset_index(drop=True)
        get_country_stats_wgi = wgi[(wgi['country_name'] == country) & (wgi['year'] == year) ].reset_index(drop=True)
        get_country_stats_fiw = fiw[(fiw['country_name'] == country) & (fiw['year'] == year) ].reset_index(drop=True)


        CC_EST = get_country_stats_wgi['CC.EST'][0]
        GE_EST = get_country_stats_wgi['GE.EST'][0]
        PV_NO_SRC = get_country_stats_wgi['PV.NO.SRC'][0]
        RL_EST = get_country_stats_wgi['RL.EST'][0]
        VA_EST = get_country_stats_wgi['VA.EST'][0]

        NF = 0
        PF = 0

        if get_country_stats_fiw['fiw_status'][0] == 'NF':
            NF = 1
        elif get_country_stats_fiw['fiw_status'][0] == 'PF':
            PF = 1


        protesterviolence=0
        if protester_violence == True:
            protesterviolence = 1
        else:
            protesterviolence = 0

        region = get_country_stats_mm['region'][0]
        asia =0
        central_america=0
        europe=0
        mena=0
        n_america=0
        oceania=0
        s_america=0

        if region == "Asia":
            asia = 1
        elif region == "Central America":
            central_america = 1
        elif region == "Europe":
            europe = 1
        elif region == "Middle East and North Africa":
            mena = 1
        elif region == 'North America':
            n_america = 1
        elif region == 'Oceania':
            oceania = 1
        elif region == 's_america':
            s_america =1


        participants_category = 1

        if participants_count == '50-99':
            participants_category = 2
        elif participants_count == '100-999':
            participants_category = 3
        elif participants_count == '1000-1999':
            participants_category = 4
        elif participants_count == '2000-4999':
            participants_category = 5
        elif participants_count == '5000-10000':
            participants_category = 6
        elif participants_count == '>10000':
            participants_category = 7
        else:
            participants_category = 1


        labor_wage_dispute = 0
        land_farm_issue = 0
        police_brutality = 0
        political_behavior_process = 0
        price_increases_tax_policy = 0
        removal_politician = 0
        social_restrictions = 0

        if motivation == 'labor wage dispute':
            labor_wage_dispute = 1
        if motivation == 'land farm issue':
            land_farm_issue = 1
        if motivation == 'police brutality':
            police_brutality = 1
        if motivation == 'political behavior, process':
            political_behavior_process = 1
        if motivation == 'price increases, tax policy':
            price_increases_tax_policy = 1
        if motivation == 'removal of politician':
            removal_politician = 1
        if motivation == 'social restrictions':
            social_restrictions = 1

        pred = stacks.predict([[year, protesterviolence, participants_category, duration,
                               labor_wage_dispute, land_farm_issue, police_brutality, political_behavior_process,
                               price_increases_tax_policy, removal_politician, social_restrictions, CC_EST, GE_EST,
                               PV_NO_SRC, RL_EST, VA_EST, asia, central_america, europe, mena, n_america,
                               oceania, s_america, NF, PF]])



        if pred == 0:               #accomodation
            outcome = " not issuing a notice. Violence is not predicted"
        elif pred == 1:             #arrests
            outcome = " issuing a notice advising that people avoid the area"
        elif pred == 2:             #beatings
            outcome = " issuing a notice."
        elif pred == 3:             #crowd dispersal
            outcome = " issuing a notice advising that people avoid the area"
        elif pred == 4:             #ignore
            outcome = " not issuing a notice. Violence is not predicted"
        elif pred == 5:             #killings
            outcome = " issuing a notice advising that people avoid the area"
        elif pred == 6:             #shootings
            outcome = " issuing a notice advising that people avoid the area"
        elif pred == 7:             #unknown
            outcome = " issuing a notice"

        return outcome





    st.write("Please answer the following questions in order to receive a prediction regarding the state response to this protest.")
    st.caption("Model has a 70% accuracy score.")
    country = st.selectbox('Country Name', country_list)
    year = st.slider('In what year is the protest taking place?', 2006, 2021, step=1)
    protesterviolence = st.checkbox('Has protester violence been witnessed up to this point?')
    duration = st.text_input("How many days has this protest been ongoing?", 1)
    participants_count = st.selectbox('How many participants are expected?', ['unknown','50-99','100-999',
    '1000-1999','2000-4999','5000-10000','>10000'])
    st.write('What are the motivating factors behind this protest?')
    motivation = st.multiselect('Select Motivations', ['labor wage dispute', 'land farm issue',
     'police brutality', 'political behavior, process', 'price increases, tax policy',
       'removal of politician', 'social restrictions'])

    if st.button("Generate a Prediction"):
        outcome = prediction(country, year, protesterviolence, participants_count, duration,
                       motivation)
        st.write(f"The model advises that you consider{outcome}.")
