from codebase_graph_latex.constants import *
developer_component_knowledge = {}

def setup_component():
    global developer_component_knowledge
    if len(developer_component_knowledge.values()) == 0:
        developer_component_knowledge[TRANSIENT_FOUNDER] = {}
        developer_component_knowledge[SUSTAINED_FOUNDER] = {}
        developer_component_knowledge[TRANSIENT_JOINER] = {}
        developer_component_knowledge[SUSTAINED_JOINER] = {}
        for component in ["packages", "files", "classes", "methods"]:
            developer_component_knowledge[TRANSIENT_FOUNDER][component] = {}
            developer_component_knowledge[SUSTAINED_FOUNDER][component] = {}
            developer_component_knowledge[TRANSIENT_JOINER][component] = {}
            developer_component_knowledge[SUSTAINED_JOINER][component] = {}        


def get_founder_transient_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[TRANSIENT_FOUNDER][component]

def get_founder_sustained_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[SUSTAINED_FOUNDER][component]

def get_joiner_transient_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[TRANSIENT_JOINER][component]

def get_joiner_sustained_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[SUSTAINED_JOINER][component]

def record_merge_knowledge(component, starter_transient_developers, starter_sustained_developers, joiner_transient_developers, joiner_sustained_developers):
    global developer_component_knowledge
    setup_component()
    get_founder_transient_component(component).update(starter_transient_developers)
    get_founder_sustained_component(component).update(starter_sustained_developers)
    get_joiner_transient_component(component).update(joiner_transient_developers)
    get_joiner_sustained_component(component).update(joiner_sustained_developers)

def merge_knowledge(component, developers):
    record_merge_knowledge(component, developers[TRANSIENT_FOUNDER], developers[SUSTAINED_FOUNDER], developers[TRANSIENT_JOINER], developers[SUSTAINED_JOINER])
   