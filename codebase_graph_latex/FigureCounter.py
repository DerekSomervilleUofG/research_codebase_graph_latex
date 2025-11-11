class FigureCounter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FigureCounter, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.counter = 0.0

    def increment_graph(self):
        self.counter += 1

    def increment_sub_graph(self):
        self.counter += 0.1

    def get_counter(self):
        return self.counter