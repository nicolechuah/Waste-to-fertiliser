class Collect():
    count_id = 0
    
    def __init__(self, name, email, type, method, address, time):
        Collect.count_id += 1
        self.__collect_id = Collect.count_id
        self.__name = name
        self.__email = email
        self.__type = type
        self.__method = method
        self.__address = address
        self.__time = time

    def set_collect_id(self, collect_id):
        self.__collect_id = collect_id

    def get_collect_id(self):
        return self.__collect_id
    def set_name(self,name):
        self.__name = name
    def get_name(self):
        return self.__name
    def set_email(self,email):
        self.__email = email
    def get_email(self):
        return self.__email
    def set_type(self,type):
        self.__type = type
    def get_type(self):
        return self.__type
    def set_method(self,method):
        self.__method = method
    def get_method(self):
        return self.__method
    def set_address(self,address):
        self.__address = address
    def get_address(self):
        return self.__address
    def set_time(self,time):
        self.__time = time
    def get_time(self):
        return self.__time