from datetime import date
from email.policy import default

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model  # Assuming you use the custom User model

# User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    subject = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    experience = models.IntegerField(default=0)  # In years
    qualification = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, default=None)
    profile_image = models.ImageField(upload_to='teacher_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"


# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    grade = models.CharField(max_length=10)
    date_of_birth = models.DateField(default=date(2000, 1, 1))
    phone_number = models.CharField(max_length=15, null=True, blank=True, default=None)
    parent_contact = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to='student_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.grade}"


# Quiz Model

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.IntegerField()  # Time in minutes
    guidelines = models.TextField(blank=True, null=True)  # New field for quiz guidelines
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField('Question', related_name='quizzes')  # Relate Quiz to multiple questions

    def total_marks(self):
        # Sum the marks of all questions related to this quiz
        return sum(question.marks for question in self.questions.all())

    def __str__(self):
        return self.title


# Course Model
class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, default="")
    difficulty_level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    duration = models.IntegerField(default=0)  # Duration in weeks
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions_in_quiz',default='')  # Unique related_name
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions_in_course',default=None)  # Unique related_name
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)  # Index (1-4)
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('true_false', 'True/False')])
    explanation = models.TextField(null=True, blank=True)
    marks = models.IntegerField()

    def __str__(self):
        return f"Q{self.id}: {self.question_text}"




# Marks Model
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='marks',default="")
    score = models.FloatField()
    grade = models.CharField(max_length=2)
    feedback = models.TextField(null=True, blank=True)
    date_taken = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title} - {self.score}"


# Teacher Application Model
class TeacherApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True, blank=True, default=None)
    resume = models.FileField(upload_to='teacher_applications/resumes/', null=True, blank=True)
    cover_letter = models.TextField()
    approved = models.BooleanField(default=False)
    applied_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {'Approved' if self.approved else 'Pending'}"


# Choice Model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice {self.id} for Question {self.question.id}"


# User Quiz Attempt Model
class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField()
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    recorded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


class UserAnswer(models.Model):
    attempt = models.ForeignKey('UserQuizAttempt', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1,default=1)  # To store '1', '2', '3', or '4'
    is_correct = models.BooleanField()  # Whether the selected option is correct


    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.id}"


# Feedback Model
class Feedback(models.Model):
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name='feedback')
    feedback_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback for {self.attempt.user.username} - {self.attempt.quiz.title}"


# Leaderboard Model
class Leaderboard(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='leaderboard')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard')
    score = models.FloatField()
    date_achieved = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Leaderboard: {self.user.username} - {self.score}"


# Settings Model
class Settings(models.Model):
    site_name = models.CharField(max_length=100, default="My Site")
    email = models.EmailField()
    description = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    logo = models.ImageField(upload_to='site_logos/', null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        return cls.objects.first() or cls.objects.create(site_name="My Site", email="info@example.com")


class StudentExam(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    exam = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    assigned_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"


class QuizAttemptHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    attempt_date = models.DateTimeField(auto_now_add=True)
