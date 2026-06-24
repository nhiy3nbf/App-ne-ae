class Major:
    def __init__(self, student_id, name, semester, course):
        self.student_id = student_id
        self.name = name
        self.semester = semester
        self. course = course
        self.student_record = {
            'E001': ['Cody', '1', 'Electronic Engineering'],
            'C002': ['Damian', '2', 'Computer Science'],
            'M003': ['Ethan', '1', 'Mechanical Engineering'],
            'C014': ['Fariana', '3', 'Civil Engineering'],
            'G005': ['Goldy', '4', 'Biomedical Engineering']
        }
    def student_verify(self, entered_id):
        if entered_id in self.student_record:
            info = self.student_record[entered_id]
            print(f'Welcome, {info[0]}! Semester {info[1]} ({info[2]})')
            return info[0]
        elif entered_id.isdigit():
            print('Access Denied: ID can not be only numbers.')
        elif entered_id.isalpha():
            print('Access Denied: ID can not only be letters.')
        else:
            print('Access Denied: ID not found in system.')
        return None
    def add_student(self, new_id, new_name, new_semester, new_course):
        if new_id in self.student_record:
            print(f'Error: {new_id} already belongs to {self.student_record[new_id][0]}')
        elif new_id.isdigit():
            print(f'Error: ID cannot consist only of numbers.')
        else:
            self.student_record[new_id] = [new_name, new_semester, new_course]
            print(f'Successfully added {new_name} with ID {new_id}')

class Course(Major):
    def __init__(self, student_id, name, semester, course, subject=None, score=None):
        super().__init__(student_id, name, semester, course)
        self.subject = subject
        self.score = score
        self.subject_record = {
            'Cody': {
                'Math': 50,
                'Science': 60,
                'Physics': 75,
                'Technology': 80,
                'Medical': None,
                'Coding_Python': 90,
                'Coding_VSC': 86,
                'Advanced_Technology_System': None,
                'Advanced_Physics_For_Mechanical_Fundamental': None
            },
            'Damian': {
                'Math': 85,
                'Science': 90,
                'Physics': 88,
                'Technology': 95,
                'Medical': None,
                'Coding_Python': 90,
                'Coding_VSC': 88,
                'Advanced_Technology_System': 76,
                'Advanced_Physics_For_Mechanical_Fundamental': None
            },
            'Ethan': {
                'Math': 45,
                'Science': 55,
                'Physics': 77,
                'Technology': 70,
                'Medical': None,
                'Coding_Python': None,
                'Coding_VSC': None,
                'Advanced_Technology_System': None,
                'Advanced_Physics_For_Mechanical_Fundamental': 88
            },
            'Fariana': {
                'Math': 92,
                'Science': 88,
                'Physics': 94,
                'Technology': 91,
                'Medical': None,
                'Coding_Python': 90,
                'Coding_VSC': 86,
                'Advanced_Technology_System': 77,
                'Advanced_Physics_For_Mechanical_Fundamental': None
            },
            'Goldy': {
                'Math': 78,
                'Science': 82,
                'Physics': 80,
                'Technology': 85,
                'Medical': 88,
                'Coding_Python': None,
                'Coding_VSC': None,
                'Advanced_Technology_System': 74,
                'Advanced_Physics_For_Mechanical_Fundamental': None
            }
        }
    '''def show_student_score(self):
        for student_name, grades_dict in self.subject_record.items():
            print(f"\nReport for {student_name}:")
            print("-" * 30)
            for subj, scr in grades_dict.items():
                if scr is not None:
                    print(f"  {subj}: {scr}")
                else:
                    print(f"  {subj}: Not Enrolled")'''
    show_student_score = lambda self, student_name: (
        print(f"\nReport for {student_name}:"),
        print("-" * 30),
        [
            print(f"  {subj}: {scr}" if scr is not None else f"  {subj}: Not Enrolled")
            for subj, scr in self.subject_record[student_name].items()
        ]
    )

current_student = Major('G005','Goldy',4,'Biomedical Engineering')

input_id = input('Verification... Enter Your Student ID: ')
verified_student = current_student.student_verify(input_id)

if verified_student:
    student_system = Course('G005', 'Goldy', 4, 'Biomedical Engineering')
    student_system.show_student_score(verified_student)
