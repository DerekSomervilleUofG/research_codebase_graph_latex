from codebase_graph_latex.constants import *

REPOSITORY_ID = 0
REPO_NAME = 1
FOUNDER_DEVELOPER_COUNT = 2
JOINER_DEVELOPER_COUNT = 3
COMMIT_COUNT = 4
MIN_DATE = 5
MAX_DATE = 6 

def query():
    select_statement = " SELECT dc.repository_id, repo.name, count(distinct ds.developer_id), "
    select_statement += " count(distinct dc.developer_id) - count(distinct ds.developer_id), count(dc.commit_id), "
    select_statement += " min(authored_date), max(authored_date)  "
    select_statement += " FROM developer_commit dc, repository repo "
    select_statement += " LEFT JOIN developer_" + FOUNDER + " ds ON dc.developer_id = ds.developer_id "
    select_statement += " WHERE dc.repository_id = repo.repository_id " 
    select_statement += " and dc.status = 'A' "
    select_statement += " AND repo.status in ('A','B') "
    select_statement += " GROUP BY dc.repository_id "
    return select_statement