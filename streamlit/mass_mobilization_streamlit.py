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


st.sidebar.title('Mass Mobilization and World Changing')
st.sidebar.subheader('A Study of the Mass Mobilization Dataset Alongside Various Indices')



page = st.sidebar.selectbox( 'Select a page', ('About', 'Data by Country', 'Case Studies', 'Time Series Model'))

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

if page == "Content Based Filtering":


    # read in dataframes
    #loan_id_df = pd.read_csv("../data/transformed/loan_id.csv")
    model_df = pd.read_csv("./streamlit_data/processed_content_filter_data.csv")
    X = pd.read_csv("./streamlit_data/X_df.csv")

    # X = model_df.drop(["user_favorite", "volunteer_like", "volunteer_pick", "rancor", "DESCRIPTION",
    #                    "LOAN_AMOUNT", "LOAN_USE", "TAGS", "TAGS+", "TEXT", "PROCESSED_TEXT", "LOAN_ID"],
    #                   axis = 1).astype(np.uint8)
    X = X.to_numpy()

    # st.set_page_config(layout="wide")

    @st.cache()


    def recommend(user):
        """
        user : numpy array

        Takes a user interests array and finds the cosine similarity between user user_interests
        and available loans.

        Sorts cosine similarity scores by greatest to least and returns the top 5 matching loan ids
        """

        # reshape user to column vector
        user = np.reshape(user, (1, -1))

        # find cosine similarity
        rec = cosine_similarity(X, user)

        # creates an ordinal that will stand in for the dataframe index to track which scores pair with
        # which index in the dataframe
        ordinals = [i for i in range(len(rec.ravel()))]
        rec_ordinal = list(zip(rec.ravel(), ordinals))

        # sorts by cosine similarity score
        sorted_index = sorted(rec_ordinal, key = lambda x: x[0], reverse=True)

        # slice
        top_loan_ids = [(x, model_df.iloc[y][0]) for x, y in sorted_index[0:5]]

        return top_loan_ids

    st.title("Content Based Filter")
    st.write("Tell us which sector interests you the most.")

    cols = st.columns(5)
    agro_sector = cols[0].checkbox("Agriculture")
    retail_sector = cols[1].checkbox("Retail")
    it_sector = cols[2].checkbox("Computers and Technology")
    education_sector = cols[3].checkbox("Education")
    health_sanitation_sector = cols[4].checkbox("Health and Sanitation")

    cols2 = st.columns(5)
    arts_sector =  cols2[0].checkbox("Arts")
    construction_sector = cols2[1].checkbox("Construction")
    entertainment_sector = cols2[2].checkbox("Entertainment")
    health_sector = cols2[3].checkbox("Health")
    manufacturing_sector = cols2[4].checkbox("Manufacturing")

    st.write("Tell us about the projects and people you are interested in by selecting 5 or more items below.")

    cols3 = st.columns(5)
    livestock = cols3[0].checkbox("Livestock")
    water = cols3[1].checkbox("Water-Filtration")
    women_owned = cols3[2].checkbox("Women-Owned Business")
    blacksmith = cols3[3].checkbox("Blacksmith")
    rrr = cols3[4].checkbox("Repair Renew Replace")

    cols4 = st.columns(5)
    dream = cols4[0].checkbox("Dream")
    female_operated = cols4[1].checkbox("Female Operated")
    school_fees_children = cols4[2].checkbox("School Fees(Young Children)")
    single_mother = cols4[3].checkbox("Single Mother")
    well_digging = cols4[4].checkbox("Well Digging")

    cols5 = st.columns(5)
    orphan = cols5[0].checkbox("Orphan")
    medical_expenses = cols5[1].checkbox("Medical: Expenses")
    textile = cols5[2].checkbox("Textiles")
    dairy = cols5[3].checkbox("Dairy")
    expand_business = cols5[4].checkbox("Expand Business")

    cols7 = st.columns(5)
    repeat_borrower = cols7[0].checkbox("Repeat Borrower")
    family = cols7[1].checkbox("Support Families")
    sanitation = cols7[2].checkbox("Sanitation")
    c19 = cols7[3].checkbox("Covid-19 Relief")
    vegan = cols7[4].checkbox("Vegan")

    cols8 = st.columns(5)
    latin = cols8[0].checkbox("Hispanic/Latinx Owned Business")
    school_fees_adoles = cols8[1].checkbox("School Fees(Adolescent)")
    sustainable = cols8[2].checkbox("Sustainable Agriculture")
    senior = cols8[3].checkbox("Senior Person(s)")
    job_creator = cols8[4].checkbox("Job Creator")

    if st.button("Fund an entrepeneur."):
        print(agro_sector)

        # an array of zeros equal in length to numbero f columns in x to examine cosine similarity with user/user user_interests
        # and available loans
        user = np.zeros(X.shape[1])

        # Pairing column number with column name allowing for manual selection and grouping user interests
        # [print(f"{i} {j}") for i, j in enumerate(X_df.columns)]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # Sector and Industry                                                                   #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


        if agro_sector == True: # = cols[0].checkbox("Agriculture")
            user[[10, 172]] = 1

        elif retail_sector == True: # = cols[1].checkbox("Retail")
            user[[16, 19, 23 , 43, 70, 92]] = 1

        elif it_sector == True: #= cols[2].checkbox("Computers and Technology")
            user[[46, 47, 91, 183]] = 1

        elif education_sector == True: #= cols[3].checkbox("Education")
            user[[176, 132]] = 1

        elif health_sanitation_sector == True: #= cols[4].checkbox("Health and Sanitation")
            user[[179, 85]] = 1

        elif arts_sector == True: # =  cols2[0].checkbox("Arts")
            user[[14, 173, 61]] = 1

        elif construction_sector == True:# = cols2[1].checkbox("Construction")
            user[[48, 49, 175]] = 1

        elif entertainment_sector == True:#= cols2[2].checkbox("Entertainment")
            user[[80, 177, 63]] = 1

        elif health_sector == True: #= cols2[3].checkbox("Health")
            user[179, 132, 102] = 1

        elif manufacturing_sector == True: #= cols2[4].checkbox("Manufacturing")
            user[[181, 101]] = 1

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Projects and People                                                                   #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        elif livestock == True: #= cols3[0].checkbox("Livestock")
            user[[187, 129, 131, 20]] = 1

        elif water == True: #= cols3[1].checkbox("Water-Filtration")
            user[[240, 228]] = 1

        elif women_owned == True: #= cols3[2].checkbox("Women-Owned Business")
            user[[222]] = 1

        elif blacksmith == True: #= cols3[3].checkbox("Blacksmith")
            user[[24]] = 1

        elif rrr == True: #= cols3[4].checkbox("Repair Renew Replace")
            user[[206, 48, 49, ]] = 1

        elif dream == True: #= cols4[0].checkbox("Dream")
            user[[227]] = 1

        elif female_operated == True: #= cols4[1].checkbox("Female Operated")
            user[[0]] = 1

        elif school_fees_children == True: #= cols4[2].checkbox("School Fees(Young Children)")
            user[[223, 224, 238, 224, 208]] = 1

        elif single_mother == True: #= cols4[3].checkbox("Single Mother")
            user[[239]] = 1

        elif well_digging == True: #= cols4[4].checkbox("Well Digging")
            user[[170]] = 1

        elif orphan == True: #= cols5[0].checkbox("Orphan")
            user[[202]] = 1

        elif medical_expenses == True: #= cols5[1].checkbox("Medical: Expenses")
            user[[236]] = 1

        elif textile == True: #= cols5[2].checkbox("Textiles")
            user[[154]] = 1

        elif dairy == True: #= cols5[3].checkbox("Dairy")
            user[[53]] = 1

        elif expand_business == True: #= cols5[4].checkbox("Expand Business")
            user[[229, 230]] = 1

        elif repeat_borrower == True: #= cols7[0].checkbox("Repeat Borrower")
            user[[207]] = 1

        elif family == True: #= cols7[1].checkbox("Support Families")
            user[[239, 235, 203, 210, 211]] = 1

        elif sanitation == True: #= cols7[2].checkbox("Sanitation")
            user[[194, 237, 234]] = 1

        elif c19 == True: #= cols7[3].checkbox("Medical: Covid-19")
            user[[225]] = 1

        elif vegan == True: #= cols7[4].checkbox("Vegan")
            user[[220]] = 1

        elif latin == True: #= cols8[0].checkbox("Hispanic/Latinx Owned Business")
            user[[199]] = 1

        elif school_fees_adoles == True: #= cols8[1].checkbox("School Fees(Adolescent)")
            user[[233, 238, 208]] = 1

        elif sustainable == True: #= cols8[2].checkbox("Sustainable Agriculture")
            user[[189, 212]] = 1

        elif senior == True: #= cols8[3].checkbox("Senior Person")
            user[[190]] = 1

        elif job_creator == True: #= cols8[4].checkbox("Job Creator")
            user[[198]] = 1


        recommendations = recommend(user)

        for i in range(0, 4):
            loan_id = recommendations[i][1]
            base_url = 'https://api.kivaws.org/graphql?query='
            graphql_query = '{lend {loan (id: %s){id name gender image {id url} description use geocode{country{name}} loanAmount sector{name}}}}'   %loan_id

            r = requests.post(base_url + graphql_query)
            r = r.json()
            url = r['data']['lend']['loan']['image']['url']
            url_600 = re.sub("s100", "s600", url)

            response = requests.get(url_600)
            img = Image.open(BytesIO(response.content))
            img.resize((500,500), Image.ANTIALIAS)

            if i in [0, 1]:
                cols = st.columns(2)
                cols[i].image(img)
                cols[i].write(f'Name: {r["data"]["lend"]["loan"]["name"]}')
                cols[i].write(f'Country: {r["data"]["lend"]["loan"]["geocode"]["country"]["name"]}')
                cols[i].write(f'Sector: {r["data"]["lend"]["loan"]["sector"]["name"]}')
                cols[i].write(f'Use: {r["data"]["lend"]["loan"]["use"].capitalize()}')
                cols[i].write(f'Loan Amount: {r["data"]["lend"]["loan"]["loanAmount"]}')
                cols[i].write("Description:")
                cols[i].write(re.sub("\\r|\\n|\\t|---|<br />", "", r["data"]["lend"]["loan"]["description"])[0:1000] + "...")


            if i in [2, 3]:
                i = i - 2
                cols2 = st.columns(2)
                cols2[i].image(img)
                cols2[i].write(f'Name: {r["data"]["lend"]["loan"]["name"]}')
                cols2[i].write(f'Country: {r["data"]["lend"]["loan"]["geocode"]["country"]["name"]}')
                cols2[i].write(f'Sector: {r["data"]["lend"]["loan"]["sector"]["name"]}')
                cols2[i].write(f'Use: {r["data"]["lend"]["loan"]["use"].capitalize()}')
                cols2[i].write(f'Loan Amount: {r["data"]["lend"]["loan"]["loanAmount"]}')
                cols2[i].write("Description:")
                cols2[i].write(re.sub("\\r|\\n|\\t|---|<br />", "", r["data"]["lend"]["loan"]["description"])[0:500] + "...")


        # for i in range(5):
        #     loan_id = recommendations[i][1]
        #     base_url = 'https://api.kivaws.org/graphql?query='
        #     graphql_query = '{lend {loan (id: %s){id name gender image {id url}  }}}'   %loan_id
        #
        #     r = requests.post(base_url+ graphql_query)
        #     r = r.json()
        #     url = r['data']['lend']['loan']['image']['url']
