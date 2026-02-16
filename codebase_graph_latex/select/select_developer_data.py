from codebase_graph_latex.constants import *

COMMIT_ID = 0
DEVELOPER_COL = 1
AUTHORED_DATE_COL = 2
COMMIT_PACKAGE_COL = 3
PACKAGE_KNOWN_COL = 4

def query(repository_id, module, type):
    select_statement = f"""
        SELECT dc.commit_id, dc.developer_id, dc.authored_date, 
        dc.number_of_repo_{module}
        , ptc.number_of_known_{module}
        FROM developer_commit dc, 
        prior_total_commit ptc, 
        developer_{type} dn 
        WHERE dc.commit_id = ptc.commit_id 
        AND dc.repository_id = dn.repository_id 
        AND dc.status in ('A', 'L') 
        AND dn.number_of_commits >= {str(NUMBER_OF_COMMIT)}
        AND dc.developer_id = dn.developer_id 
        AND dc.repository_id = {str(repository_id)}
        ORDER BY dc.developer_id, dc.authored_date
        """
    return select_statement