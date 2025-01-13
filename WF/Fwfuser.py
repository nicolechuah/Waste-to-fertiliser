import shelve
class FWFUser:
    count_id =0
    def __init__(self, first_name, last_name, gender,email, remarks=''):
        FWFUser.count_id += 1
        self.__fwfuser_id = FWFUser.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__remarks = remarks
        self.__email = email
    def set_fwfuser_id(self,fwfuser_id):
        self.__fwfuser_id = fwfuser_id
    def get_fwfuser_id(self):
        return self.__fwfuser_id
    def set_first_name(self,first_name):
        self.__first_name = first_name
    def get_first_name(self):
        return self.__first_name
    def set_last_name(self,last_name):
        self.__last_name = last_name
    def get_last_name(self):
        return self.__last_name
    def set_gender(self,gender):
        self.__gender = gender
    def get_gender(self):
        return self.__gender
    def set_remarks(self,remarks):
        self.__remarks = remarks
    def get_remarks(self):
        return self.__remarks
    def set_email(self,email):
        self.__email = email
    def get_email(self):
        return self.__email