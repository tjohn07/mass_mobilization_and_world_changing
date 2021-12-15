
# Predicting Protest Outcomes:
## A Study of the Mass Mobilization Dataset Alongside Various Indices

By: erri John


This ReadMe contains:

* [Project Contents](#contents)
* [Problem Statement](#problemstatement)
* [Project Planning and Methodology](#planning)
* [A description of the data and Project Requirements](#data)
* [Modeling and Analysis](#model)
* [Conclusion](#conclusion)
* [Sources](#sources)
* [Data Dictionary](#dict)


## <a name="contents"></a>Project Contents:

|Name|Description|
|---|---|
|1_EDA_Cleaning|Cleans and merges data from 3 sources. Initial EDA.|
|2_Case_Studies|A closer look at a few countries.|
|3_Classification Model|Builds various classification models.|
|4_Visualizations|A visual exploration of the data.|
|data|folder containing csv files of data used|
|streamlit|folder containing streamlit.py file, folder with streamlit images, folder with streamlit data files|

## <a name="problemstatement"></a>Problem Statement and Background

When a protest takes place overseas, Diplomatic Security officers need to make a decision as to whether or not the protest warrants alerting the USG community, and in particular whether or not they will recommend that people avoid the area of the protest. Based on this decision, Consular Officers need to decide whether or not the protest warrants sending a message to the American citizen community - a MASCOT message. While this may sound simple, as with all things related to diplomacy it can become complicated. If we err on the side of sending a notice every time we are alerted of a planned protest, we risk causing offense to the host nation or the local populace. If we err on the side of sending fewer notifications, there is a chance that someone could inadvertently find themselves caught in the middle of a dangerous situation that they otherwise could have avoided with proper warning. Typically, officers rely on their local expertise to make these decisions. This is effective, but leaves room for personal bias. I’ve seen messages go out for protests with only 3 participants, and I’ve seen no messages go out for protests that ended with hundreds of participants marching through a residential area while setting off fireworks. In response to this need, I’ve developed a model that will help overseas personnel make data driven decisions. The resulting model isn’t perfect, but coupled with the expertise of our overseas personnel it can lead to better, more informed decision making. It’s simply another tool in the Foreign Service Officer toolkit.


## <a name="planning"></a>Project Planning and Methodology

Preparation for exploring this data involved considerable trial and error. I was particularly interested in bringing in various metrics from the World Bank's Databank, particularly those related to World Governance Indicators, GDP, and Poverty and Equity Indicators. After careful consideration, I felt obligated to drop use of the GDP and Poverty and Equity indicators. The data included too many nulls and would have led to considerable loss of data across merges with the Mass Mobilization and World Governance Indicator datasets. I do feel that this is an area for further focus. With more time, I would perform closer analysis and cleaning of the Poverty and Equity indicators, as well as the available GDP data, so that the data may become more useful.

For this study, I am limiting my data to the years 2006-2021, since these are the years that align across all 3 data sources. I may consider breaking into early data in other capacities in the future.

I will also take this moment to note that unfortunately the Mass Mobilization dataset does not include data for the United States or Australia.

## <a name="data"></a>Data:

### Get the Data:
* The data for this study came from 3 sources:
  * Mass Mobilization Project Dataverse: https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/HTTWYL/TJJZNG&version=5.0
  * Freedom House: https://freedomhouse.org/countries/freedom-world/scores
  * WorldBank Databank: https://databank.worldbank.org/home.aspx

For ease of use and given the complicated cleaning process, the data files are uploaded to GitHub and saved under:
 data --> transformed

 Several lines of code in Notebook 1 (EDA/Cleaning) have been commented out for ease of you.  If you wish to run through the full cleaning process, uncomment those lines.

Data Dictionaries Available from the Respective Sources:
Mass Mobilization: https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/HTTWYL/TJJZNG&version=5.0

World Governance Indicators: In the metadata file

Freedom in the World:

|column|description|
|---|---|
|year|year of given designation|
|country|designated country name|
|fiw_score|not free, partially free, or free|


### Project Requirements:   
* streamlit==1.1.0
* joblib==1.1.0
* scikit-learn==1.0.1
* matplotlib==3.5.0
* numpy==1.21.2
* pandas==1.3.4
* seaborn==0.11.2


## <a name="model"></a>Modeling and Analysis
I created 2 classification models:
1. [Binary Classification: A model to predict protester violence](#binary)
2. [Multiclass Classification: A model to predict state response](#multi)

|Model|Null Model|Train Accuracy|Test Accuracy|F1 Score|
|---|---|---|---|---|
|Binary Classification: KNN|74%|82%|82%|72%|
|Multiclass Classficiation: Stacked|53%|70%|70%|66%

### <a name="binary"></a>  Binary Classification Model



### <a name="multi"></a> Multiclass Classification Model



## <a name="conclusion"></a>Conclusion:
### Limitations and Recommendations for next steps:
* Bring in more metrics to include in the modeling process. The WorldBank Databank has a lot of interesting data that could be brought in. I looked at several metrics that I thought would be interesting to include, but there were too many nulls. With more time, we can evaluate these nulls and pull in more metrics.
* Perform time series modeling. My initial goal for this project was to exame the long and short term effects of protests, and this is something that I hope to pursue in the future.
* Improve the data cleaning process to minimize loss of data - this will involve some manual cleaning.




### <a name="sources"></a>Sources

* Mass Mobilization Project Dataverse: https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/HTTWYL/TJJZNG&version=5.0
* Freedom House: https://freedomhouse.org/countries/freedom-world/scores
* WorldBank Databank: https://databank.worldbank.org/home.aspx
* Wikipedia: Tunisian Protests: https://en.wikipedia.org/wiki/2018_Tunisian_protests
