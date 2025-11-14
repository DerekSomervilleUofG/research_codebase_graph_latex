from codebase_graph_latex.constants import *
DEVELOPER_ID = 0
COUNT = 1

def query(type):
    select_statement = " SELECT dc.developer_id, count(dc.commit_id)  "
    select_statement += " FROM developer_commit dc, developer_" + type + " dt"
    select_statement += " WHERE dc.repository_id = dt.repository_id " 
    select_statement += " and dc.status = 'A' "
    select_statement += " AND dc.developer_id = dt.developer_id " 
    select_statement += " AND dt.number_of_commits >= " + str(NUMBER_OF_COMMIT)
    select_statement += " GROUP BY dc.developer_id "
    return select_statement

if __name__ == "__main__":
    print(query(3, "joiner"))