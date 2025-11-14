from codebase_graph_latex.constants import *
developer_component_knowledge = {}

def setup_component():
    global developer_component_knowledge
    if len(developer_component_knowledge.values()) == 0:
        developer_component_knowledge[FOUNDER] = {}
        developer_component_knowledge[FOUNDER][TRANSIENT] = {}
        developer_component_knowledge[FOUNDER][SUSTAINED] = {}
        developer_component_knowledge[JOINER] = {}
        developer_component_knowledge[JOINER][TRANSIENT] = {}
        developer_component_knowledge[JOINER][SUSTAINED] = {}
        for component in ["packages", "files", "classes", "methods"]:
            developer_component_knowledge[FOUNDER][TRANSIENT][component] = {}
            developer_component_knowledge[FOUNDER][SUSTAINED][component] = {}
            developer_component_knowledge[JOINER][TRANSIENT][component] = {}
            developer_component_knowledge[JOINER][SUSTAINED][component] = {}        


def get_founder_transient_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[FOUNDER][TRANSIENT][component]

def get_founder_sustained_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[FOUNDER][SUSTAINED][component]

def get_joiner_transient_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[JOINER][TRANSIENT][component]

def get_joiner_sustained_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[JOINER][SUSTAINED][component]

def record_merge_knowledge(component, starter_transient_developers, starter_sustained_developers, joiner_transient_developers, joiner_sustained_developers):
    global developer_component_knowledge
    setup_component()
    get_founder_transient_component(component).update(starter_transient_developers)
    get_founder_sustained_component(component).update(starter_sustained_developers)
    get_joiner_transient_component(component).update(joiner_transient_developers)
    get_joiner_sustained_component(component).update(joiner_sustained_developers)

def merge_knowledge(component, developers):
    record_merge_knowledge(component, developers[TRANSIENT_FOUNDER], developers[SUSTAINED_FOUNDER], developers[TRANSIENT_JOINER], developers[SUSTAINED_JOINER])
   