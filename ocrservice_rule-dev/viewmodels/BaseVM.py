import repository as repo

class BaseVM:
    def __init__(self):
        self.general_apps = repo.get_general_apps()
        self.user_apps = repo.get_user_apps()
        