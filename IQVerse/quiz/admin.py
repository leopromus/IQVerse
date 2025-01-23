from django.contrib import admin
from .models import (
    Teacher, Student, Course, Question, Marks, TeacherApplication, User,
    Quiz, Choice, UserQuizAttempt, UserAnswer, Feedback, Leaderboard, Settings, QuizAttemptHistory, Testimonial
)

# Register all models using admin.site.register
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Marks)
admin.site.register(TeacherApplication)
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Choice)
admin.site.register(UserQuizAttempt)
admin.site.register(UserAnswer)
admin.site.register(Feedback)
admin.site.register(Leaderboard)
admin.site.register(Settings)
admin.site.register(QuizAttemptHistory)
admin.site.register(Testimonial)





