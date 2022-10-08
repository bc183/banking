class UserStore:
    _user = None

    @staticmethod
    def set_user(user):
        UserStore._user = user

    @staticmethod
    def get_user():
        if UserStore._user is None:
            print("User is not logged in")
            exit()
        return UserStore._user
