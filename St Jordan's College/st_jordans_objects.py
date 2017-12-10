class Student(object):
    def __init__(self, first_name, surname, student_id):
        self.first_name = first_name
        self.surname = surname
        self.student_id = student_id
        self.behaviour_slips = []
        # self.tutor = None
    '''
    def routine_check(self):
        return len(self.behaviour_slips) >= 3

class Teacher(object):
    def __init__(self, teacher_id, department):
        self.teacher_id = teacher_id
        self.department = department
        self.is_HOD = False

    def add_behaviour(self, student, behaviour):
        # Behaviour Incident Slips in the form: (Name) Behaviour: (Behaviour) Verified=False
        return (student.first_name + ' ' + student.surname, 'Behaviour:', behaviour, False)

    def file_behaviour(self, slip, student):
         student.behaviour_slips.append(slip)
        

class HOD(Teacher):
    def __init__(self, teacher_id, department):
        super(HOD, self).__init__(name, department)
        self.is_HOD = True
        
    def verify(behaviour):
        return True

class Tutor(Teacher):
    def __init__(self, teacher_id, department, students):
        super(Tutor, self).__init__(name, department)
        self.students = students
        for student in students:
            student.tutor = self
'''
def s():
    school = []
    for line in open('students.txt'):
        line = line.strip().split()
        school.append(Student(line[1], line[2], int(line[0])))
    return school
school = s()
