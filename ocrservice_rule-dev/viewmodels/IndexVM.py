from viewmodels.BaseVM import BaseVM

class IndexVM(BaseVM):
    def __init__(self):
        self.features = []
        self.top_rule = ""
        self.bot_rule = ""
        self.split = ""
        self.app_name = ""
        super(IndexVM, self).__init__()
    def set_rules(self, rules):
        if rules == None:
            rules = []
        if "top_rule" in rules:
            self.top_rule = "checked"
        if "bot_rule" in rules:
            self.bot_rule = "checked"
        if "split_rule" in rules:
            self.split_rule = "checked"
            
    def set_features(self, features):
        if features != None:
            self.features = features
        else:
            self.features = []