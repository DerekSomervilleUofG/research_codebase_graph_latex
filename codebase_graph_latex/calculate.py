import pandas as pd
import datetime
from codebase_graph_latex.constants import *
import numpy as np
CAPTION_LENGTH = 100
BREADTH = 1
INTER = 2
DEPTH = 3
BREADTH_THRESHOLD = 10.0
DEPTH_THRESHOLD = 25.0
MINIMUM_DEPTH = 5

def filter_developers(developers):
    return {key: value for key, value in developers.items() if len(value[NUMBER_OF_COMMIT]) >= DEVELOPER_HAS_NUMNER_OF_COMMITS and value[YEAR_PERIOD][-1] >= DEVELOPER_PERIOD}

def filter_developers_by_commits(developers, number_of_commits):
    return {key: value for key, value in developers.items() if len(value[NUMBER_OF_COMMIT]) >= number_of_commits}


def get_date_time(date_time):
    return datetime.datetime.strptime(date_time, "%Y%m%d%H%M%S")

def get_date(date_time):
    return datetime.datetime.strptime(date_time, "%Y%m%d%H%M%S").date()

def days_difference(first_date_time, second_date_time):
    delta = get_date(first_date_time) - get_date(second_date_time) 
    return abs(delta.days) + 1

def get_integer(number):
    result = 0
    if number.isnumeric():
        result = int(number)
    return result

def calc_percentage(number, base):
    percentage = 0
    if base > 0:
        percentage = (int(number)/base)*100
    return percentage
    
def merge_dictionary(first_dictionary, second_dictionary, third_dictionary={}, fourth_dicictionary={}, fifth_dictionary={}):
    merged_dictionary = {}
    merged_dictionary.update(first_dictionary)
    merged_dictionary.update(second_dictionary)
    merged_dictionary.update(third_dictionary)
    merged_dictionary.update(fourth_dicictionary)
    merged_dictionary.update(fifth_dictionary)      
    return merge_dictionary

def find_developer_unit(unit):
    if unit == NUMBER_OF_MONTHS:
        return DEV_MONTH
    elif unit == NUMBER_OF_WEEKS:
        return DEV_WEEK
    elif unit == TIME_SERIES_NUMBER_OF_COMMIT:
        return DEV_COMMIT
    else:
        return DEV_COMMIT

def add_extra(target_list, number_extra, value=0):
    for counter in range(0, number_extra):
        target_list.append(value)

def categorize_ratio(ratio, packages_touched, number_of_commits):
    if (pd.isna(ratio) or ratio < BREADTH_THRESHOLD) and packages_touched > (number_of_commits//2) + 2:
        return BREADTH
    elif ratio >= DEPTH_THRESHOLD and packages_touched <= min((number_of_commits//2) + 2, MINIMUM_DEPTH):
        return DEPTH
    else:
        return INTER