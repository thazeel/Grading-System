# Open Files
model_answer = open(r"Model_Answer.txt", "r")
student_answer = open(r"Student_Answer.txt", "r")

# Read Data from Files
model = model_answer.read()
student = student_answer.read()

# Printing the Data
print("Model Answer\n===========\n", model)
print("\n\nStudent Answer\n==============\n", student)
