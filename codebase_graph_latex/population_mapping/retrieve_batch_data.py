from repository_save.population_mapping.PopulateTable import PopulateTable

BATCH_SIZE = 1000
populate_table = None
entity_cursor = None

def initialise_populate_table(control_populate):
    global populate_table
    populate_table = PopulateTable(control_populate.db_execute_sql)

def has_next():
    return populate_table.has_next

def prepare_batch_select(select_query):
    global entity_cursor
    entity_cursor = populate_table.prepare_batch_select(select_query)
    populate_table.has_next = True

def next_batch_select():
    return populate_table.next_batch_select(entity_cursor, BATCH_SIZE)

def get_all_data(select_query):
    all_record = []
    entity_cursor = populate_table.prepare_batch_select(select_query)
    populate_table.has_next = True
    while populate_table.has_next:
        batch_of_records = populate_table.next_batch_select(entity_cursor, BATCH_SIZE)
        all_record += batch_of_records
    return all_record
