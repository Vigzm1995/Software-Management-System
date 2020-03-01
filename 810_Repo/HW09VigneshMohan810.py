'''
    File Name: HW09VigneshMohan (810).py
    Script Author: Vignesh Mohan
    Purpose: Week 9 Assignment.
    Python Version: 3.0
'''

''' Program to create stevens students data repository'''

import unittest
import os 
from collections import defaultdict
from prettytable import PrettyTable
from HW08VigneshMohan_Part2_810 import file_read

class Repository:

    #def file_reader(self, path, num_fields, expect, sep = '\t', header = False):
        
    #Functions used to store information about the students and instructors.
    def __init__(self, wdir, ptables = True):

        self._wdir = wdir #Creating a new directory to store information of students, instructors and grades.
        self._students = dict() #Class instance for students.
        self._instructors = dict() #Class instance for instructors.

        #Lines of code to read information from various files associated to students, instructors and grades.
        self._get_students(os.path.join(wdir, 'students.txt')) 
        self._get_instructors(os.path.join(wdir, 'instructors.txt')) 
        self._get_grades(os.path.join(wdir, 'grades.txt')) 

        #Pretty table to print the student and instructor summary.
        if ptables:
            print ('\n Student Summary')
            self.student_table()

            print ('\n Instructor Summary')
            self.instructor_table()
    
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
                    self._students[cwid] = Student(cwid, name, major)
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
            #Grades file with Student CWID, course and grade and also instructor CWID.
            for student_cwid, course, grade, instructors_cwid in file_read(path, 4, sep = '\t', header = False):
                #Displays students new updated course and grades.
                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade) 
                else:
                    #Invalid CWID, not on file.
                    print (f' Warning: student cwid {student_cwid} is not known in the file') 
            
                #Instructor updates students on their respective course and grades.
                if instructors_cwid in self._instructors:
                    self._instructors[instructors_cwid].add_course(course) 
                else:
                    print (f' Warning: instructor cwid {instructors_cwid} is not known in the file') 
        except ValueError as error:
            print (error) 

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

#Class Student for initialization, course addition and display as a pretty table.
class Student:
    
    #Pretty Table to display a single students details.
    pt_lables = ['CWID', 'Name','Major', 'Completed courses']

    def __init__(self, cwid, name, major):
        
        #Initialization of student labels.
        self._cwid = cwid
        self._name = name
        self._major = major

        self._courses = dict() #key : courses value: str with grade
        #self.lables = ['CWID', 'Name', 'course', 'courses']

    def add_course(self, course, grade):
        #Assigning a respective grade to a particular student.
        self._courses[course] = grade
    
    def pt_row(self):
        #Value list returned to add a new row to the student table.
        return [self._cwid, self._name, self._major, sorted(self._courses.keys())]
    
    #def __str__(self):
        #return f'Student: {self._cwid} name: {self._name} course: {self._course} courses: {sorted(self._courses.keys())}'


#Class Instructor for initialization, adding students and display as a pretty table rows.
class Instructor:
    
    #Pretty table with respective instructor labels.
    pt_labels = ['CWID', 'Name', 'Department', 'Course', 'Students']

    #Initialization of instructor labels.
    def __init__(self, cwid, name, dept):

        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int) #key : courses value: no. of students in the course

    def add_course(self, course):
        #Counter for instructor to add additional courses to respective students.
        self._courses[course] += 1

    def pt_row(self):
        for course, students in self._courses.items():
            #Yield function to print the respective CWID, name, department and course.
            yield [self._cwid, self._name, self._dept, course, students]

'''
#Unit test cases for class student.
class Student_Test(unittest.TestCase):
    def test_student_test(self):

        stevens = Repository("Users\Vignesh\PycharmProjects\HW09VigneshMohan (810)\Repository")
        student_details = [s.pt_row() for s in stevens._students.values()]
        #Printing the student details.
        print (student_details)
'''
      
def main():
    
    '''
    #Specifying the file path.
    _wdir = 'Users\Vignesh\PycharmProjects\HW09VigneshMohan (810)\Repository'
    stevens = Repository(_wdir)
    unittest.main(exit=False)
    '''
    Repository("Users\Vignesh\PycharmProjects")

if __name__ == '__main__':

    main()
    #unittest.main(exit=False, verbosity=2)

