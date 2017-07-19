class Action(Exception):
    """description of class"""
    def __init__(self, label, **kwargs):
        self.description = label
        return super().__init__(**kwargs)