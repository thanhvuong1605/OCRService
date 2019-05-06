from viewmodels.BaseVM import BaseVM

class CreateAppVM(BaseVM):
    def __init__(self):
        self.features = []
        super(CreateAppVM, self).__init__()