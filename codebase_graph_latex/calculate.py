import datetime

CAPTION_LENGTH = 100


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
