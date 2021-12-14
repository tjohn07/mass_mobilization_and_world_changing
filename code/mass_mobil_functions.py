import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from sklearn.model_selection import train_test_split, cross_val_predict, GridSearchCV
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn import metrics 

# encoding categorical columns prior to modeling.

def categorical_to_encode(df,  columns_to_label_encode, columns_to_get_dummies):
    '''
    function to apply LabelEncoder and/or GetDummies to prepare dataframe for modeling.
    Inputs:
    df = a dataframe
    columns_to_label_encode: a list of columns to apply LabelEncoder
    columns_to_get_dummies: a list of columns to apply GetDummies
    Output:
    an encoded data frame ready for modeling.
    '''
    #resetting 'duration' column to remove letters, resulting in a numeric column

    for column in columns_to_label_encode:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
    for column in columns_to_get_dummies:
        dummy_df = pd.get_dummies(df[column], drop_first=True)
        df = pd.concat([df, dummy_df], axis=1)

    df.drop(columns = columns_to_get_dummies, inplace=True)

    return df


def time_series_by_country(df, place, agg_method = 'sum', interval = 'MS'):

    '''
    A function to downsample the full dataframe to view data by country.
    Date range will include all years for which data is available for a specified country.
    Input:
        * a dataframe - defaults to 'df'
        * place - country or region name
        * agg_method - aggregation method for resampling. defaults to 'sum'. 'mean' also recommended.
        * interval - 'YS': annual / 'MS': monthly. Default is monthly.

    '''
    try:
        # generate downsamples dataframe based on country selection
        output_df = df[df['country_name'] == place.title()]

        #set index to date_time based on protest startdate
        output_df = output_df.sort_values(by='start_date')
        output_df.set_index(pd.DatetimeIndex(output_df['start_date']), inplace=True)

        #specify date range if desired
        start_date = str(output_df.index.min())[:4]
        end_date = str(output_df.index.max())[:4]
        output_df = output_df.loc[start_date:end_date]

        output_df.drop(columns = ['year', 'end_date', 'ccode', 'country_name', 'start_date', 'duration'], inplace=True)

        # resample to look at data based on regular intervals
        output_df.resample(interval).protest.agg(agg_method)


        return output_df

    except:

        print(f'We don\'t have enough data to fulfill your request for {place}. Please check your spelling, or try another location.')

def model_metrics(some_lr, scaled=False):

    if scaled:
        train_r2 = some_lr.score(X_train_sc, y_train)
        test_r2 = some_lr.score(X_test_sc, y_test)
    else:

        train_r2 = some_lr.score(X_train, y_train)
        test_r2 = some_lr.score(X_test, y_test)
    preds = some_lr.predict(X)
    resids_mean = (y - preds).mean()
    mae = metrics.mean_absolute_error(y, preds)
    resids = resids = y - preds
    rss = (resids ** 2).sum()
    mse = metrics.mean_squared_error(y, preds)
    rmse = np.sqrt(metrics.mean_squared_error(y, preds))
    cvs = cross_val_score(some_lr, X, y, cv=5).mean()

    final_dict={'Train R2 Score': train_r2,
                'Test R2 Score' : test_r2,
                'Mean of Residuals': resids_mean,
               'Mean Absolute Error': mae,
               'Residual Sum of Squares': rss,
               'Mean Squared Error': mse,
               'Root Mean Squared Error': rmse,
               'cross_val_score': cvs}
    return final_dict
