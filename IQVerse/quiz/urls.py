from django.urls import path
from . import views

urlpatterns = [
    # 📝 List and Create Quizzes
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/create/', views.quiz_create, name='quiz_create'),

    # ❓ Quiz Detail (Get Questions and Choices)
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

    # 🧑‍🎓 Start Quiz Attempt
    path('quizzes/<int:quiz_id>/start/', views.start_quiz_attempt, name='start_quiz_attempt'),

    # ✅ Submit Answers for Quiz Attempt
    path('attempts/<int:attempt_id>/submit/', views.submit_answers, name='submit_answers'),

    # 🔗 View Leaderboard for Quiz
    path('quizzes/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
]
