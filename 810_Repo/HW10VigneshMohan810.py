'''
    File Name: HW10VigneshMohan (810).py
    Script Author: Vignesh Mohan
    Purpose: Week 10 Assignment.
    Python Version: 3.0
'''

''' Program to create stevens students data repository'''

import os
from collections import defaultdict
from prettytable import PrettyTable
import unittest
from HW08VigneshMohan_Part2_810 import file_read
from HW09VigneshMohan810 import file_read

class Repository:

    #def file_reader(self, path, num_fields, expect, sep = '\t', header = False):
        
    #Functions used to store information about the students and instructors.
    def __init__(self, wdir, ptables = True):

        self._wdir = wdir #Creating a new directory to store information of students, instructors and grades.
        self._students = dict() #Class instance for students.
        self._instructors = dict() #Class instance for instructors.
        self._majors = dict() #Class instance for majors.

        #Lines of code to read information from various files associated to students, instructors and grades.
        self._get_students(os.path.join(wdir, 'students.txt')) 
        self._get_instructors(os.path.join(wdir, 'instructors.txt')) 
        self._get_grades(os.path.join(wdir, 'grades.txt')) 
        self._get_majors(os.path.join(wdir, 'majors.txt')) 
        
        #Pretty table to print the student and instructor summary.
        if ptables:
            print ('\n Student Summary')
            self.student_table()

            print ('\n Instructor Summary')
            self.instructor_table()

            print ('\n Major Summary')
            self.major_table()

    #'_get_students' function to read students from path and ad  to self.students.
    def _get_students(self, path):
        
        try:
            #Studen file with CWID, name and major.
            for cwid, name, major in file_read(path, 3, sep = '\t', header = False):
                #Warning for cwid duplication if present in self._students.
                if cwid in self._students:
                    print (f' Warning: cwid {cwid} already read from the file')
                #Print student's CWID, name and major.
                else:
                    self._students[cwid] = Student(cwid, name, major, self._majors[major])
        except ValueError as error:
            print(error)


    #'_get_instructors' function to read instructors from path and add to self.instructors.
    def _get_instructors(self, path):

        try:
            #Instructor file with CWID, name and department.
            for cwid, name, dept in file_read(path, 3, sep = '\t', header = False):
                #Warning for cwid duplication if present in self._instructors.
                if cwid in self._instructors:
                    print (f' Warning: cwid {cwid} already read from the file')
                #Print instructors CWID, name and deptartment.
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as error:
            print(error)

  
    #'_get_grades' function for students and instructors operations
    def _get_grades(self, path):
    
        try:
            #Grades file with Student CWID, coursese and grade and also instructor CWID.
            for student_cwid, coursese, grade, instructors_cwid in file_read(path, 4, sep = '\t', header = False):
                #Displays students new updated coursese and grades.
                if student_cwid in self._students:
                    self._students[student_cwid].add_coursese(coursese, grade) 
                else:
                    #Invalid CWID, not on file.
                    print (f' Warning: student cwid {student_cwid} is not known in the file') 
            
                #Instructor updates students on their respective coursese and grades.
                if instructors_cwid in self._instructors:
                    self._instructors[instructors_cwid].add_coursese(coursese) 
                else:
                    print (f' Warning: instructor cwid {instructors_cwid} is not known in the file') 
        except ValueError as error:
            print (error) 


    def _get_majors(self, path):
        try:
            for major, course, flag in file_read(path, 3, sep = "\t", header = False):
                if major in self._majors:
                    self._majors[major].add_course(flag, course)
                else:
                    self._majors[major] = Major(major)

        except ValueError as err:
            print(err)

     #'student_table' function to print summary of students as a pretty table.    
    def student_table(self):
    
        pt = PrettyTable(field_names = Student.pt_lables)
        for student in self._students.values():
            pt.add_row(student.pt_row())

        #Printing the pretty table.
        print(pt)
    
    #'instructor_table' function to print summary of instructors as a pretty table.
    def instructor_table(self):
    
        pt = PrettyTable(field_names = Instructor.pt_labels)
        for instructor in self._instructors.values():
            for row in instructor.pt_rows():
                pt.add_row(row)
        
        #Printing Pretty Table.
        print(pt)
    
    def major_table(self):
        
        pt = PrettyTable(field_names = Major.pt_labels)
        for major in self._majors.values():
            pt.add_row(major.pt_row())

        print(pt)


class Student:

    #Pretty Table to display a single students details.
    pt_lables = ['CWID', 'Name','Major', 'Completed courseses']

    def __init__(self, cwid, name, major, in_major):
        self._cwid = cwid
        self._name = name
        #self._majors = major
        self._inmajor = in_major
        self._courseses = dict()  
        
        self._major = major
        self._inmajor = in_major

    def add_coursese(self, coursese, grade):
        #List of grades.
        grades_list = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        if grade in grades_list:
            #Assigning a respective grade to a particular student.
            self._courseses[coursese] = grade

    def pt_row(self):

        courses_completed, required_remaining, courses_remaining = self._inmajor.grade_check(self._courseses)
        #Value list returned to add a new row to the student table.
        return[self._cwid, self._name, self._major, sorted(courses_completed), required_remaining, courses_remaining]

#Class Instructor for initialization, adding students and display as a pretty table rows.
class Instructor:

    #Pretty table with respective instructor labels.
    pt_labels = ['CWID', 'Name', 'Department', 'coursese', 'Students']

    def __init__(self, cwid, name, dept):
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courseses = defaultdict(int) # key: coursese value: number of students

    
    def add_coursese(self, coursese):
        #Counter for instructor to add additional courseses to respective students.
        self._courseses[coursese] += 1

    def pt_row(self):
        for coursese, students in self._courseses.items():
            #Yield function to print the respective CWID, name, department and coursese.
            yield [self._cwid, self._name, self._dept, coursese, students]

class Major:
    pt_labels = ["Major", "Required Courses", "Electives"]
    
    def __init__(self, major, passing=None):
        self._major = major
        self._required = set()
        self._elective = set()

        if passing is None:
            self._passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        else:
            self._passing_grades = passing

    def add_coursese(self, fl, coursese):

        if fl == 'R':
            self._required.add(coursese)
        elif fl == 'E':
            self._elective.add(coursese)
        else:
            raise ValueError(f"unexcepted flag {fl} in majors.txt")

    def grade_check(self, courseses):
        courses_completed = {courseses for courseses, gd in courseses.items() if gd in self._passing_grades}
        if courses_completed == "{}":
            return[courses_completed, self._required, self._elective]
        else:
            required_remaining = self._required - courses_completed
            if self._elective.intersection(courses_completed):
                courses_remaining = None
            else:
                courses_remaining = self._elective

            return[courses_completed, required_remaining, courses_remaining]

    def pt_row(self):

        return[self._major, self._required, self._elective]


def main():

    wdir = 'Users\Vignesh\PycharmProjects'
    stevens = Repository(wdir)

#Unit Test Cases.
class RepositoryTest(unittest.TestCase):
    
    def test_stevens(self):
        
        wdir = 'Users\Vignesh\PycharmProjects'
        stevens = Repository(wdir, False)
        expected_student = [["10103", "Baldwin, C", "SFEN", ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None], ["10172", "Forbes, I", "SFEN", ['SSW 555', 'SSW 567'], {'SSW 564', 'SSW 540'}, {'CS 545', 'CS 501', 'CS 513'}], ["10115", "Wyatt, X", "SFEN", ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None],]
        expected_instructor = [["98765", "Einstein, A", "SFEN", "SSW 567", 4], ["98765", "Einstein, A", "SFEN", "SSW 540", 3], ["98764", "Feynman, R", "SFEN", "CS 501", 1], ["98764", "Feynman, R", "SFEN", "SSW 564", 3], ["98764", "Feynman, R", "SFEN", "SSW 687", 3]]
        
        expected_major = [["SFEN", {'SSW 540', 'SSW 564', 'SSW 567', 'SSW 555'}, {'CS 545', 'CS 501', 'CS 513'}], ["SYEN", {'SYS 612', 'SYS 800', 'SYS 671'}, {'SSW 810', 'SSW 565', 'SSW 540'}]]
        
        ptable_student = [s.pt_row() for s in stevens._students.values()]
        ptable_instructor = [row for Instructor in stevens._instructors.values() for row in Instructor.pt_row()]
        ptable_major = [m.pt_row() for m in stevens._majors.values()]

        self.assertEqual(ptable_major, expected_major)
        self.assertEqual(ptable_student, expected_student)
        self.assertEqual(ptable_instructor, expected_instructor)


if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)
