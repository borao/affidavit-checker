import csv
import os
import re
import database


class Main(object):
    entries_csv = ""
    registered_students = []
    matched_students = []
    matched_students_as_string = []
    unverified_and_unrecorded = []
    verified = []

    def __init__(self):
        for file in os.listdir(os.getcwd()):
            if ".csv" in file:
                self.entries_csv = file

    def get_registered_students(self):
        csv_doc = csv.reader(open(self.entries_csv))
        next(csv_doc)
        for row in csv_doc:
            if row[13]:
                self.registered_students.append(row[13])
            if row[14]:
                self.registered_students.append(row[14])
            if row[15]:
                self.registered_students.append(row[15])
        return self.registered_students

    def strip_grade_levels(self):
        for i, this_student in enumerate(self.registered_students):
            self.registered_students[i] = re.sub("\d+", "", this_student)
        return self.registered_students

    def sort_registered_students(self):
        self.registered_students = sorted(self.registered_students)
        return self.registered_students

    def compare_registered_to_db(self, db_students):
        for student in self.registered_students:
            for i, db_student in enumerate(db_students):
                if db_students[i][1] == student and \
                        db_student[1] not in self.matched_students_as_string:
                    self.matched_students.append(db_students[i])
                    self.matched_students_as_string.append(db_students[i][1])

    def get_unverified_and_unrecorded(self):
        for student in self.matched_students:
            if student[0].affidavit_verified != "1":
                self.unverified_and_unrecorded.append(student)
            else:
                self.verified.append(student)
        for student in self.registered_students:
            if student not in self.matched_students_as_string:
                self.unverified_and_unrecorded.append(student)
        return self.verified, self.unverified_and_unrecorded


if __name__ == '__main__':
    db_students = database.Database().list_student_names_strings()
    Main().get_registered_students()
    Main().strip_grade_levels()
    Main().sort_registered_students()
    Main().compare_registered_to_db(db_students)
    verified_and_unverified = Main().get_unverified_and_unrecorded()
    verified = verified_and_unverified[0]
    unverified = verified_and_unverified[1]
    percent_verified = (len(verified) / (
            len(verified) + len(unverified))) * 100

    f = open("status.txt", "w")
    f.write("* Statistics\n")
    f.write("  {0:.0f}% of registrants verified\n".format(percent_verified))
    f.write("\n* Verified Students:\n")
    for student in verified:
        f.write("  {}\n".format(student[1]))
    f.write("\n* Unverified Students:\n")
    for student in unverified:
        f.write("  {}\n".format(student))
