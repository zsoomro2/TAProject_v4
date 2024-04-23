from course import Course
import unittest

class TestInit(unittest.TestCase):
    #name tests
    def test_noName(self):
        with self.assertRaises(Exception,msg="No name provided")
    a = Course("",100,"12:00","1:00",3,test_Instructor, test_TA)
    
    def test_invalidNameInt(self):
        with self.assertRaises(Exception,msg="Invalid name")
    a = Course(1,100,"12:00","1:00",3,test_Instructor, test_TA)
    
    def test_invalidNameFloat(self):
        with self.assertRaises(Exception,msg="Invalid name")
    a = Course(1.0,100,"12:00","1:00",3,test_Instructor, test_TA)
    
    def test_invalidNameChar(self):
        with self.assertRaises(Exception,msg="Invalid name")
    a = Course('a',100,"12:00","1:00",3,test_Instructor, test_TA)
    
    #section tests
    def test_noSection(self):
        with self.assertRaises(Exception,msg="No section provided")
    a = Course("name",0,"12:00","1:00",3,test_Instructor, test_TA)
    
    def test_invalidSectionFloat(self):
        with self.assertRaises(Exception,msg="Invalid sectino")
    a = Course("name",1.0,"12:00","1:00",3,test_Instructor, test_TA)
    
    def test_invalidSectionChar(self):
        with self.assertRaises(Exception,msg="Invalid section")
    a = Course("name",'a',"12:00","1:00",3,test_Instructor, test_TA)
    
    #start tests
    def test_noStart(self):
        with self.assertRaises(Exception,msg="No start provided")
    a = Course("",100,"","1:00",3,test_Instructor, test_TA)
    
    def test_invalidStartInt(self):
        with self.assertRaises(Exception,msg="Invalid start")
    a = Course(1,100,12,"1:00",3,test_Instructor, test_TA)
    
    def test_invalidStartFloat(self):
        with self.assertRaises(Exception,msg="Invalid start")
    a = Course(1.0,100,12.00,"1:00",3,test_Instructor, test_TA)
    
    def test_invalidStartChar(self):
        with self.assertRaises(Exception,msg="Invalid start")
    a = Course('a',100,"a","1:00",3,test_Instructor, test_TA)
    
    #end tests
    def test_noEnd(self):
        with self.assertRaises(Exception,msg="No end provided")
    a = Course("",100,"12:00","",3,test_Instructor, test_TA)
    
    def test_invalidEndInt(self):
        with self.assertRaises(Exception,msg="Invalid end")
    a = Course(1,100,"12:00",1,3,test_Instructor, test_TA)
    
    def test_invalidEndFloat(self):
        with self.assertRaises(Exception,msg="Invalid end")
    a = Course(1.0,100,"12:00",1.0,3,test_Instructor, test_TA)
    
    def test_invalidEndChar(self):
        with self.assertRaises(Exception,msg="Invalid end")
    a = Course('a',100,"12:00","a",3,test_Instructor, test_TA)
    
    #credit tests
    def test_noCredits(self):
        with self.assertRaises(Exception,msg="No credits provided")
    a = Course("",100,"12:00","1:00",0,test_Instructor, test_TA)
    
    def test_invalidCreditsInt(self):
        with self.assertRaises(Exception,msg="Invalid credits")
    a = Course(1,100,"12:00","1:00",-3,test_Instructor, test_TA)
    
    def test_invalidCreditsFloat(self):
        with self.assertRaises(Exception,msg="Invalid credits")
    a = Course(1.0,100,"12:00","1:00",3.0,test_Instructor, test_TA)
    
    def test_invalidCreditsChar(self):
        with self.assertRaises(Exception,msg="Invalid credits")
    a = Course('a',100,"12:00","1:00",'3',test_Instructor, test_TA)
    
    #instructor tests
    def test_noInstructor(self):
        with self.assertRaises(Exception,msg="No instructor provided")
    a = Course("",100,"12:00","1:00",3, Null, test_TA)
    
    def test_invalidInstructorInt(self):
        with self.assertRaises(Exception,msg="Invalid instructor")
    a = Course(1,100,"12:00","1:00",3,1, test_TA)
    
    def test_invalidInstructorFloat(self):
        with self.assertRaises(Exception,msg="Invalid instructor")
    a = Course(1.0,100,"12:00","1:00",3,1.0, test_TA)
    
    def test_invalidInstructorChar(self):
        with self.assertRaises(Exception,msg="Invalid instructor")
    a = Course('a',100,"12:00","1:00",3,'a', test_TA)
    
    #TA tests
    def test_noTA(self):
        with self.assertRaises(Exception,msg="No TA provided")
    a = Course("",100,"12:00","1:00",3, test_Instructor, Null)
    
    def test_invalidTAInt(self):
        with self.assertRaises(Exception,msg="Invalid TA")
    a = Course(1,100,"12:00","1:00",3,test_Instructor, 1)
    
    def test_invalidTAFloat(self):
        with self.assertRaises(Exception,msg="Invalid TA")
    a = Course(1.0,100,"12:00","1:00",3,test_Instructor, 1.0)
    
    def test_invalidTAChar(self):
        with self.assertRaises(Exception,msg="Invalid TA")
    a = Course('a',100,"12:00","1:00",3,test_Instructor, 'a')
