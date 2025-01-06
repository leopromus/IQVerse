from datetime import timezone

from django.contrib.auth.models import User
from django.db import models

# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    is_approved = models.BooleanField(default=False)  # Approval status for the teacher
    subject = models.CharField(max_length=100)  # Subject taught by the teacher

    def __str__(self):
        return self.user.username  # Return the username for easy identification

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    grade = models.CharField(max_length=10)  # Grade of the student

    def __str__(self):
        return self.user.username  # Return the username for easy identification

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)  # Title of the course
    description = models.TextField()  # Detailed description of the course
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Link to the teacher who teaches the course

    def __str__(self):
        return self.title  # Return the course title for easy identification

# Question Model
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link to the course this question belongs to
    question_text = models.CharField(max_length=500)  # The question text
    option1 = models.CharField(max_length=200)  # Option 1 for MCQ
    option2 = models.CharField(max_length=200)  # Option 2 for MCQ
    option3 = models.CharField(max_length=200)  # Option 3 for MCQ
    option4 = models.CharField(max_length=200)  # Option 4 for MCQ
    correct_option = models.IntegerField()  # Index of the correct option (1-4)
    marks = models.IntegerField()  # Marks for this question

    def __str__(self):
        return self.question_text  # Return the question text for easy identification

# Marks Model
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the student who took the exam
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link to the course the student is enrolled in
    score = models.IntegerField()  # The score obtained in the exam
    date_taken = models.DateTimeField(auto_now_add=True)  # Date and time when the exam was taken

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"  # Display the student username and course title

# Teacher Application Model

class TeacherApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255,default='')
    email = models.EmailField(default="<EMAIL>",)
    resume = models.FileField(upload_to='resumes/',default='resumes/default.png')
    cover_letter = models.TextField(default='',)
    approved = models.BooleanField(default=False)
    applied_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {('Approved' if self.approved else 'Pending')}"
