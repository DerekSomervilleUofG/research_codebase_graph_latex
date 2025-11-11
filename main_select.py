from codebase_graph_latex.select.select_developer_commit import query as developer_commit_query
from codebase_graph_latex.select.select_developer_data import query as developer_data_query
from codebase_graph_latex.select.select_repository_summary_table import query as repository_summary_table_query
from codebase_graph_latex.select.select_repositpory_pull_request import query as repositpory_pull_request_query



def format_query(query):
    for key_word in ["and", "where", "from", "order by", "select"]:
        query = query.replace(key_word, "\n" + key_word.upper())
        query = query.replace(key_word.upper(), "\n" + key_word.upper())
    return query

print("developer commit", format_query(developer_commit_query(3, "joiner")))
print()
print("developer data", format_query(developer_data_query(14, "packages", "joiner")))
print()
print("repository_summary_table_query", format_query(repository_summary_table_query()))
print()
print("repositpory_pull_request_query", format_query(repositpory_pull_request_query(3)))