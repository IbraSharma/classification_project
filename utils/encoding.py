
import pandas as pd
import numpy as np


def encode_categorical(df_subset):
    # Dividing the features into categorical and continuous variables
    categorical_feature = [feature for feature in df_subset.columns if df_subset[feature].dtype == 'object']
    continuous_feature = [feature for feature in df_subset.columns if df_subset[feature].dtype != 'object']
    df_cat = df_subset[categorical_feature]
    df_num = df_subset[continuous_feature]


    df_cat['year']=df_cat['reservation_status_date'].str.split('-',expand=True)[0].astype(str).astype(int)
    df_cat['month']=df_cat['reservation_status_date'].str.split('-',expand=True)[1].astype(str).astype(int)
    df_cat.drop('reservation_status_date',axis=1,inplace=True)


    # List of nominal categorical features to encode using One-Hot Encoding (pd.get_dummies)
    nominal_categorical_features = ['hotel', 'meal', 'market_segment', 'distribution_channel', 'reserved_room_type','arrival_date_month',
                                    'deposit_type', 'customer_type']

    # One-Hot Encoding for nominal categorical features
    df_encoded = pd.get_dummies(df_cat, columns=nominal_categorical_features)

    return df_encoded, df_num