import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 

def string_splitting(val):
    """
    Trims the date/time format down to desired date-only.
    """
    val = val.split(":")
    val = val[0].split("T")
    val = val[0]

    return val


def ids_list(df):
    """
    Returns the possible user id's as a list.
    """
    ids = []
    id_col = df["patient_id"]
    for id in id_col:
        if id not in ids:
            ids.append(id)
    
    return ids


def date_user_created(df, id):
    """
    Returns the date the user given was created.
    """
    rows = df.loc[df["patient_id"] == id]
    row_num = df[df["patient_id"] == id].index[0]
    date = rows.at[row_num, "patient_date_created"]
    date = string_splitting(date)

    return date

def assessment_dates_scores(df, id):
    """
    Returns the dates and scores of the user's assessments.
    """
    rows = df.loc[df["patient_id"] == id]
    dates_scores = rows[["date", "score"]]
    dates_scores_list = dates_scores.values.tolist()
    for i in range(0,len(dates_scores_list)):
        dates_scores_list[i][0] = string_splitting(dates_scores_list[i][0]) 
    new_df = pd.DataFrame(dates_scores_list, columns=["date", "score"])
    
    return new_df


def filter_dupes(df):
    """
    Filters the duplicates of the passed dataframe.
    """
    new_df = df.drop_duplicates(subset=['date'], keep='last', inplace=False)

    return new_df

def graph(df, id):
    """
    Creates a plot of the scores vs. dates of tests taken.
    """
    plt.figure()
    plt.plot(df['date'], df['score'], marker='o', linestyle='dashed')
    plt.title("Patient " + str(id) + " assessments over time.")
    plt.yticks(np.arange(0,8))
    plt.xlabel('Date of Assessment')
    plt.ylabel('Score')

    plt.show()
    return