REPOSITORY_ID = 0
STATUS = 1

def query():
    select_statement = " SELECT repository_id, STATUS "
    select_statement += " FROM repository "
    select_statement += " WHERE status in ('A', 'B') "
    select_statement += " ORDER BY status DESC, repository_id ASC; "
    return select_statement