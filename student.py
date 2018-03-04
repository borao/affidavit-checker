class Student(object):

    def __init__(self, first_name, last_name, affidavit_verified):
        self.first_name = first_name
        self.last_name = last_name
        self.affidavit_verified = affidavit_verified

    def mark_as_verified(self):
        self.affidavit_verified = True
