from codebase_graph_latex.population_mapping.retrieve_batch_data import *
from codebase_graph_latex.constants import *
from codebase_graph_latex.calculate import *
from codebase_graph_latex.select.select_developer_data import *
import copy
import math

YEAR_PERIOD = 0
KNOWN_Y_AXIS = 1
PERCENTAGE_KNOWN = 2
NUMBER_OF_COMMIT = 3
DEV_MONTH = 4
DEV_MONTH_TOUCHED = 5
DEV_WEEK = 6
DEV_WEEK_TOUCHED = 7
START_DATE = 8
AXIS_NAME = {YEAR_PERIOD: "day", KNOWN_Y_AXIS: "component touched", NUMBER_OF_COMMIT: "commits"}
PERIOD = "period"

max_commits = 0
developer_total_commit = 0
max_total_known = 0



def calc_percentage_from_row(row):
    return calc_percentage(row[PACKAGE_KNOWN_COL], row[COMMIT_PACKAGE_COL])

def get_data_from_database(repository_id, module, contributor_stage):
    global max_commits, developer_total_commit, max_total_known
    max_commits = 0
    developer_total_commit = 0
    max_total_known = 0
    developers = {}
    developers_start = None
    start_known = 0
    prepare_batch_select(query(repository_id, module, contributor_stage))
    while has_next():
        commits = next_batch_select()
        developers, developers_start, start_known = generate_data(commits, developers, developers_start, start_known)
    return developers, developer_total_commit, max_total_known 

def find_developer_unit(unit):
    if unit == NUMBER_OF_MONTHS:
        return DEV_MONTH
    else:
        return DEV_WEEK

def populate_period_touched(value, period_touched, unit):
    previous_mean = 0
    if len(value[find_developer_unit(unit) + 1]) > 0:
        previous_mean = value[find_developer_unit(unit) + 1][-1]
    while len(value[find_developer_unit(unit) + 1]) < len(value[find_developer_unit(unit)]) -1:
        value[find_developer_unit(unit) + 1].append(previous_mean)
    if len(period_touched[unit]) > 0:
        mean = sum(period_touched[unit])/len(period_touched[unit])
    else:
        mean = previous_mean
    if len(value[find_developer_unit(unit) + 1]) < unit:    
        value[find_developer_unit(unit) + 1].append(mean)
    period_touched[unit] = []
    return mean

def populate_period(value, period_touched, unit):
    mean = populate_period_touched(value, period_touched, unit)
    last_period = len(value[find_developer_unit(unit)]) -1
    for period in range(last_period + 1, unit):
        value[find_developer_unit(unit) + 1].append(mean)
    last_period = value[find_developer_unit(unit)][-1]
    for period in range(last_period + 1, unit + 1):
        value[find_developer_unit(unit)].append(period)

def populate_remaining_periods(value, period_touched):
    populate_period(value, period_touched, NUMBER_OF_MONTHS)
    populate_period(value, period_touched, NUMBER_OF_WEEKS)

def generate_data(commits, developers, developers_start, start_known):
    global max_commits, developer_total_commit, max_total_known
    template = [[1],[],[],[1],[1],[],[1],[], "" ]
    developer_id = 0
    period_touched = {NUMBER_OF_WEEKS:[], NUMBER_OF_MONTHS:[], str(NUMBER_OF_WEEKS) + PERIOD:0, str(NUMBER_OF_MONTHS) + PERIOD:0}
    previous_day = 1
    previous_knowledge = 1
    for row in commits:
        temp_developer_id = int(row[DEVELOPER_COL])
        if temp_developer_id > 0 and row[PACKAGE_KNOWN_COL] is not None:
            if temp_developer_id != developer_id:
                if developer_id in developers:
                    populate_remaining_periods(developers[developer_id], period_touched)
            developer_id = temp_developer_id
            if developer_id in developers:
                if row[AUTHORED_DATE_COL].isnumeric():
                    previous_day = days_difference(row[AUTHORED_DATE_COL], developers_start)
                else:
                    previous_day = developers[developer_id][YEAR_PERIOD][-1]
                developers[developer_id][YEAR_PERIOD].append(previous_day)
                if developers[developer_id][KNOWN_Y_AXIS][-1] > row[PACKAGE_KNOWN_COL]:
                    previous_knowledge = developers[developer_id][KNOWN_Y_AXIS][-1]
                else:
                    previous_knowledge = row[PACKAGE_KNOWN_COL]
                developers[developer_id][KNOWN_Y_AXIS].append(previous_knowledge)
                developers[developer_id][PERCENTAGE_KNOWN].append(calc_percentage(row[PACKAGE_KNOWN_COL], start_known))
                developers[developer_id][NUMBER_OF_COMMIT].append(developers[developer_id][NUMBER_OF_COMMIT][-1] + 1)
                for unit in [NUMBER_OF_MONTHS, NUMBER_OF_WEEKS]:
                    current_period = math.ceil((previous_day/ 365) * unit)
                    period_touched[str(unit) + PERIOD]= current_period
                    last_period = developers[developer_id][find_developer_unit(unit)][-1]
                    if current_period < last_period:
                        pass
                    elif current_period > last_period:
                        mean = populate_period_touched(developers[developer_id], period_touched, unit)
                        for period in range(last_period + 1, current_period):
                            developers[developer_id][find_developer_unit(unit)].append(period)
                            developers[developer_id][find_developer_unit(unit) + 1].append(mean)
                        developers[developer_id][find_developer_unit(unit)].append(current_period)
                    period_touched[unit].append(previous_knowledge)
                    
                max_commits += 1
                if max_commits > DEVELOPER_HAS_NUMNER_OF_COMMITS and row[PACKAGE_KNOWN_COL] > max_total_known:
                    max_total_known = row[PACKAGE_KNOWN_COL]
                if max_commits > developer_total_commit:
                    developer_total_commit = max_commits
            else:
                max_commits = 1
                developers_start = row[AUTHORED_DATE_COL]
                developers[developer_id] = copy.deepcopy(template)
                developers[developer_id][START_DATE] = get_date_time(row[AUTHORED_DATE_COL]).strftime('%d-%b-%Y')
                developers[developer_id][KNOWN_Y_AXIS].append(row[PACKAGE_KNOWN_COL])   
                developers[developer_id][PERCENTAGE_KNOWN].append(calc_percentage_from_row(row))
                if len(developers[developer_id][NUMBER_OF_COMMIT]) > developer_total_commit:
                    developer_total_commit = len(developers[developer_id][NUMBER_OF_COMMIT])
                start_known = row[COMMIT_PACKAGE_COL]
    populate_remaining_periods(developers[developer_id], period_touched)
    return developers, developers_start, start_known