from repository_save.Main import Main as RepositoryMain
from codebase_graph_latex.repo_graph import *
import sys

class Main(RepositoryMain):

    exclusive_lock = True

    def __init__(self):
        super().__init__()
        self.repository_id = 0
    
    def __init__(self) -> None:
        super().__init__()
 
    def process_database(self, control_populate):
        super().process_database(control_populate)
        generate_repo_latex(control_populate, self.repository_id)


        
if __name__ == "__main__":
    main = Main()
    if len(sys.argv) > 1:
        main.repository_id = int(sys.argv[1])
    #Is debugging
    elif sys.gettrace() is not None or 'debugpy' in sys.modules: 
        main.repository_id = 21
    else:
        main.repository_id = 0
    directory = "resource/database/codebase_start.db"  
    main.main(directory)
