import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
from csv_analysis import *

csv = pd.read_csv("data/phq_all_final.csv")

user_ids = ids_list(csv)

flag = False
while flag != True:
    id = int(input("Patient Id: "))
    if id not in user_ids:
        print("User Id does not exist. Try again.")
    else:
        flag = True

date_created = date_user_created(csv, id)

assess_dates_scores = assessment_dates_scores(csv, id)

filtered = filter_dupes(assess_dates_scores)

graph(filtered, id)