import psycopg2
import student
import os


class Database(object):
    students = []

    def __init__(self):
        connection = psycopg2.connect(database=os.environ['DATABASE'],
                                      user=os.environ['USER'],
                                      password=os.environ['PASSWORD'],
                                      host=os.environ['HOST'],
                                      port="5432")

        self.cursor = connection.cursor()
        self.get_students_in_db()

    def get_students_in_db(self):
        self.cursor.execute(
            "SELECT firstname, lastname, contract FROM ocdl.student ORDER BY lastname")
        rows = self.cursor.fetchall()
        for row in rows:
            self.students.append(student.Student(row[0], row[1], row[2]))
        self.sort_students_in_db()

    def sort_students_in_db(self):
        self.students.sort(key=lambda x: x.first_name)
        return self.students

    def list_student_names_strings(self):
        for i, this_student in enumerate(self.students):
            self.students[i] = (this_student,
                                this_student.first_name + " " + this_student.last_name)
        return self.students
