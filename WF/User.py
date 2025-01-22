class User:
    def __init__(self, user_id, username, email, password, profile_picture='default.jpg', is_admin=False):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__password = password
        self.__profile_picture = profile_picture
        self.__is_admin = is_admin

    def get_user_id(self):
        return self.__user_id
    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_profile_picture(self):
        return self.__profile_picture
    def is_admin(self):
        return self.__is_admin

    def set_user_id(self, user_id):
        self.__user_id = user_id
    def set_username(self, username):
        self.__username = username
    def set_email(self, email):
        self.__email = email
    def set_password(self, password):
        self.__password = password
    def set_profile_picture(self, profile_picture):
        self.__profile_picture = profile_picture
    def set_admin(self, is_admin):
        self.__is_admin = is_admin
