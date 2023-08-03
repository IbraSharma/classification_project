import pandas as pd
import numpy as np

def preprocess_data(df_subset):
    # Remove fully duplicated rows and keep only the first occurrence
    df_subset = df_subset.drop_duplicates(keep='first')

    # Impute null values for 'country', 'children', and 'agent':
    df_subset.fillna(0, inplace=True)
    df_subset["children"].fillna(0, inplace=True)
    df_subset["children"].fillna(df_subset["children"].mode()[0], inplace=True)  # float  most have 0 so it will be 0.
    df_subset["agent"].fillna(0, inplace=True)
    df_subset['agent'] = np.where(df_subset['agent'].isnull(), 0, df_subset['agent'])  # float.
    df_subset["country"].fillna(df_subset["country"].mode()[0], inplace=True)  # in any case we will remove it.
    df_subset['meal'].replace("Undefined", "SC", inplace=True)  # SC = Undefined is the same > No meal package

    # Total_guests
    df_subset['Total_guests'] = df_subset['adults'] + df_subset['children'] + df_subset['babies']
    no_guests = df_subset['Total_guests'] == 0
    df_subset = df_subset[~no_guests]
    df_subset.drop('Total_guests', axis=1, inplace=True)

    # Total staying
    df_subset['total_stay'] = df_subset['stays_in_weekend_nights'] + df_subset['stays_in_week_nights']
    no_nights = df_subset['total_stay'] == 0
    num_zero_nights = no_nights.sum()
    df_subset = df_subset[~no_nights]
    df_subset.drop('total_stay', axis=1, inplace=True)



    # Converting columns to appropriate datatypes
    df_subset[['children', 'company', 'agent']] = df_subset[['children', 'company', 'agent']].astype('int64')

    # Drop columns
    # Data Leakage: reservation_status is similar values to the target variable
    # Data Leakage: reservation_status_date
    useless_col = ['arrival_date_week_number', 'arrival_date_year', 'arrival_date_day_of_month', 'assigned_room_type', 'company',
                   'booking_changes', 'reservation_status', 'country']
    df_subset.drop(useless_col, axis=1, inplace=True)

    return df_subset