from codebase_graph_latex.constants import *

DEVELOPER_ID = 0
COUNT = 1

def query(repository_id):
    select_statement = " SELECT dn.developer_id, count(de.developer_experience_id)  "
    select_statement += " FROM developer_joiner dn, developer_experience de "
    select_statement += " WHERE dn.developer_id = de.developer_id "
    select_statement += " AND dn.number_of_commits >= " + str(NUMBER_OF_COMMIT)
    select_statement += " AND dn.repository_id = " + str(repository_id)
    select_statement += " GROUP BY dn.developer_id "
    return select_statement