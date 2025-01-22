# from rest_framework import serializers
# from .models import (
#     Teacher, Student, Course, Question, Marks, TeacherApplication, User,
#     Quiz, Choice, UserQuizAttempt, UserAnswer, Feedback, Leaderboard
# )
#
# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'is_active', 'date_joined']
#
#
# # Teacher Serializer
# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = ['id', 'user', 'subject', 'is_approved', 'experience']
#
#
# # Student Serializer
# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'user', 'grade', 'date_of_birth', 'phone_number']
#
#
# # Course Serializer
# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ['id', 'teacher', 'title', 'description', 'created_at', 'updated_at']
#
#
# # Question Serializer
# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['id', 'quiz', 'text', 'points', 'created_at']
#
#
# # Marks Serializer
# class MarksSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Marks
#         fields = ['id', 'student', 'course', 'marks', 'date_awarded']
#
#
# # Teacher Application Serializer
# class TeacherApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TeacherApplication
#         fields = ['id', 'user', 'subject', 'experience', 'status', 'application_date']
#
#
# # Quiz Serializer
# class QuizSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Quiz
#         fields = ['id', 'title', 'description', 'time_limit', 'created_at', 'updated_at']
#
#
# # Choice Serializer
# class ChoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Choice
#         fields = ['id', 'question', 'text', 'is_correct']
#
#
# # User Quiz Attempt Serializer
# class UserQuizAttemptSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserQuizAttempt
#         fields = ['id', 'user', 'quiz', 'score', 'completed', 'started_at', 'completed_at']
#
#
# # User Answer Serializer
# class UserAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAnswer
#         fields = ['id', 'attempt', 'question', 'choice', 'is_correct']
#
#
# # Feedback Serializer
# class FeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feedback
#         fields = ['id', 'attempt', 'feedback_text', 'created_at']
#
#
# # Leaderboard Serializer
# class LeaderboardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Leaderboard
#         fields = ['id', 'quiz', 'user', 'score', 'date_achieved']
