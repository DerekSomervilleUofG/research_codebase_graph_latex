from codebase_graph_latex.constants import *

COMMIT_ID = 0
DEVELOPER_COL = 1
AUTHORED_DATE_COL = 2
COMMIT_PACKAGE_COL = 3
PACKAGE_KNOWN_COL = 4

def query(repository_id, module, type):
    select_statement = " SELECT dc.commit_id, dc.developer_id, dc.authored_date, "
    select_statement += " dc.number_of_repo_" + module
    select_statement += " , ptc.number_of_known_" + module
    select_statement += " FROM developer_commit dc, "
    select_statement += " prior_total_commit ptc, "
    select_statement += " developer_" + type + " dn "
    select_statement += " WHERE dc.commit_id = ptc.commit_id "
    select_statement += " AND dc.repository_id = dn.repository_id "
    select_statement += " AND dc.status = 'A' "
    select_statement += " AND dn.number_of_commits >= " + str(NUMBER_OF_COMMIT)
    select_statement += " AND dc.developer_id = dn.developer_id "
    select_statement += " AND dc.repository_id = " + str(repository_id)
    select_statement += " ORDER BY dc.developer_id, dc.authored_date "
    return select_statement