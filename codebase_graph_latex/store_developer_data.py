from codebase_graph_latex.constants import *
developer_component_knowledge = {}

def setup_component():
    global developer_component_knowledge
    if len(developer_component_knowledge.values()) == 0:
        developer_component_knowledge[TRANSIENT_FOUNDER] = {}
        developer_component_knowledge[SUSTAINED_FOUNDER] = {}
        developer_component_knowledge[TRANSIENT_JOINER] = {}
        developer_component_knowledge[SUSTAINED_JOINER] = {}
        developer_component_knowledge[MODERATE_FOUNDER] = {}
        developer_component_knowledge[MODERATE_JOINER] = {}
        for component in ["packages", "files", "classes", "methods"]:
            developer_component_knowledge[TRANSIENT_FOUNDER][component] = {}
            developer_component_knowledge[SUSTAINED_FOUNDER][component] = {}
            developer_component_knowledge[TRANSIENT_JOINER][component] = {}
            developer_component_knowledge[SUSTAINED_JOINER][component] = {}        
            developer_component_knowledge[MODERATE_FOUNDER][component] = {}
            developer_component_knowledge[MODERATE_JOINER][component] = {}  

def get_transient_founder_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[TRANSIENT_FOUNDER][component]

def get_sustained_founder_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[SUSTAINED_FOUNDER][component]

def get_moderate_founder_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[MODERATE_FOUNDER][component]

def get_moderate_joiner_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[MODERATE_JOINER][component]

def get_transient_joiner_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[TRANSIENT_JOINER][component]

def get_sustained_joiner_component(component):
    global developer_component_knowledge
    return developer_component_knowledge[SUSTAINED_JOINER][component]

def record_merge_knowledge(component, transient_founder_developers, sustained_founder_developers, 
                           moderate_founder, moderate_joiner, 
                           joiner_transient_developers, joiner_sustained_developers):
    global developer_component_knowledge
    setup_component()
    get_transient_founder_component(component).update(transient_founder_developers)
    get_moderate_founder_component(component).update(moderate_founder)
    get_sustained_founder_component(component).update(sustained_founder_developers)
    get_transient_joiner_component(component).update(joiner_transient_developers)
    get_moderate_joiner_component(component).update(moderate_joiner)
    get_sustained_joiner_component(component).update(joiner_sustained_developers)

def merge_knowledge(component, developers):
    record_merge_knowledge(component, 
                           developers[TRANSIENT_FOUNDER], developers[SUSTAINED_FOUNDER], 
                           developers[MODERATE_FOUNDER], developers[MODERATE_JOINER], 
                           developers[TRANSIENT_JOINER], developers[SUSTAINED_JOINER])
   