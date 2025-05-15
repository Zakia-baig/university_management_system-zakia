import json

class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

class Student(Person):
    def __init__(self, name, age, gender, roll_number, email):
        super().__init__(name, age, gender)
        self.roll_number = roll_number
        self.email = email

class Professor(Person):
    def __init__(self, name, age, gender, employee_id, department):
        super().__init__(name, age, gender)
        self.employee_id = employee_id
        self.department = department

class Course:
    def __init__(self, code, name, professor_id, capacity):
        self.code = code
        self.name = name
        self.professor_id = professor_id
        self.capacity = capacity
        self.students = []

class University:
    def __init__(self):
        self.students = {}
        self.professors = {}
        self.courses = {}
    
    def add_student(self, student):
        if student.roll_number in self.students:
            print("Error: Student already exists!")
            return
        self.students[student.roll_number] = student
    
    def add_professor(self, professor):
        if professor.employee_id in self.professors:
            print("Error: Professor already exists!")
            return
        self.professors[professor.employee_id] = professor
    
    def add_course(self, course):
        if course.code in self.courses:
            print("Error: Course already exists!")
            return
        self.courses[course.code] = course
    
    def enroll_student(self, roll_number, course_code):
        if roll_number in self.students and course_code in self.courses:
            course = self.courses[course_code]
            if roll_number in course.students:
                print("Student already enrolled.")
                return False
            if len(course.students) >= course.capacity:
                print("Course is full.")
                return False
            course.students.append(roll_number)
            return True
        return False
    
    def withdraw_student(self, roll_number, course_code):
        if course_code in self.courses and roll_number in self.courses[course_code].students:
            self.courses[course_code].students.remove(roll_number)
            return True
        return False

    def save_data(self, filename):
        data = {
            "students": {roll: vars(s) for roll, s in self.students.items()},
            "professors": {emp_id: vars(p) for emp_id, p in self.professors.items()},
            "courses": {code: {"name": c.name, 
                               "professor_id": c.professor_id,
                               "capacity": c.capacity,
                               "students": c.students} 
                        for code, c in self.courses.items()}
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        self.students = {
            roll: Student(s["name"], s["age"], s["gender"], roll, s["email"])
            for roll, s in data["students"].items()
        }

        self.professors = {
            emp_id: Professor(p["name"], p["age"], p["gender"], emp_id, p["department"])
            for emp_id, p in data["professors"].items()
        }

        self.courses = {}
        for code, c in data["courses"].items():
            course = Course(code, c["name"], c["professor_id"], c["capacity"])
            course.students = c["students"]
            self.courses[code] = course

def show_menu():
    print("\n--- University Management System ---")
    print("1. Add Student")
    print("2. Add Professor")
    print("3. Add Course")
    print("4. Enroll Student")
    print("5. Withdraw Student")
    print("6. View All Data")
    print("7. Save Data")
    print("8. Load Data")
    print("9. Exit")

def main():
    uni = University()
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            student = Student(
                name=input("Name: "),
                age=int(input("Age: ")),
                gender=input("Gender: "),
                roll_number=input("Roll Number: "),
                email=input("Email: ")
            )
            uni.add_student(student)
        
        elif choice == "2":
            professor = Professor(
                name=input("Name: "),
                age=int(input("Age: ")),
                gender=input("Gender: "),
                employee_id=input("Employee ID: "),
                department=input("Department: ")
            )
            uni.add_professor(professor)
        
        elif choice == "3":
            course = Course(
                code=input("Course Code: "),
                name=input("Course Name: "),
                professor_id=input("Professor ID: "),
                capacity=int(input("Course Capacity: "))
            )
            uni.add_course(course)
        
        elif choice == "4":
            if uni.enroll_student(input("Student Roll Number: "), input("Course Code: ")):
                print("Enrolled successfully!")
            else:
                print("Enrollment failed.")
        
        elif choice == "5":
            if uni.withdraw_student(input("Student Roll Number: "), input("Course Code: ")):
                print("Withdrawal successful!")
            else:
                print("Withdrawal failed.")
        
        elif choice == "6":
            print("\nStudents:")
            for s in uni.students.values():
                print(f"{s.roll_number}: {s.name}, {s.age} y/o, {s.gender}, Email: {s.email}")
            print("\nProfessors:")
            for p in uni.professors.values():
                print(f"{p.employee_id}: {p.name}, {p.age} y/o, {p.gender}, Dept: {p.department}")
            print("\nCourses:")
            for c in uni.courses.values():
                print(f"{c.code}: {c.name}, Prof: {c.professor_id}, Capacity: {c.capacity}")
                print(" Enrolled Students:", ", ".join(c.students) if c.students else "None")

        elif choice == "7":
            uni.save_data(input("Enter filename to save: "))
            print("Data saved successfully.")
        
        elif choice == "8":
            uni.load_data(input("Enter filename to load: "))
            print("Data loaded successfully.")
        
        elif choice == "9":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

