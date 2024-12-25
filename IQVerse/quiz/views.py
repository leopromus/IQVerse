from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Quiz, Question, UserQuizAttempt, UserAnswer, Feedback, Leaderboard
from .serializers import QuizSerializer, QuestionSerializer, UserQuizAttemptSerializer, UserAnswerSerializer, \
    FeedbackSerializer, LeaderboardSerializer
from django.contrib.auth import get_user_model

# Get the default User model
User = get_user_model()


# 📝 1. List all quizzes
@api_view(['GET'])
def quiz_list(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)


# 📝 2. Create a new quiz
@api_view(['POST'])
def quiz_create(request):
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ❓ 3. Get quiz details with questions and choices
@api_view(['GET'])
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    question_serializer = QuestionSerializer(questions, many=True)
    quiz_serializer = QuizSerializer(quiz)
    return Response({
        'quiz': quiz_serializer.data,
        'questions': question_serializer.data
    })


# 🧑‍🎓 4. Start a quiz attempt for a user
@api_view(['POST'])
def start_quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_attempt = UserQuizAttempt.objects.create(user=request.user, quiz=quiz)
    serializer = UserQuizAttemptSerializer(user_attempt)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ✅ 5. Submit answers for a quiz attempt
@api_view(['POST'])
def submit_answers(request, attempt_id):
    attempt = get_object_or_404(UserQuizAttempt, id=attempt_id)
    answers = request.data.get('answers', [])
    total_score = 0
    for answer_data in answers:
        question = get_object_or_404(Question, id=answer_data['question_id'])
        choice = get_object_or_404(Choice, id=answer_data['choice_id'])
        is_correct = choice.is_correct
        user_answer = UserAnswer.objects.create(
            attempt=attempt,
            question=question,
            choice=choice,
            is_correct=is_correct
        )
        if is_correct:
            total_score += question.points

    attempt.score = total_score
    attempt.completed = True
    attempt.save()

    # Create feedback
    feedback_text = f"Your total score is {total_score}. Good job!" if total_score >= 50 else "Keep practicing, you can do better!"
    feedback = Feedback.objects.create(attempt=attempt, feedback_text=feedback_text)

    # Update leaderboard
    leaderboard_entry = Leaderboard.objects.create(quiz=attempt.quiz, user=attempt.user, score=total_score)

    return Response({
        'message': 'Quiz submitted successfully!',
        'score': total_score,
        'feedback': feedback_text
    })


# 🔗 6. View the leaderboard for a quiz
@api_view(['GET'])
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    leaderboard = Leaderboard.objects.filter(quiz=quiz).order_by('-score')
    serializer = LeaderboardSerializer(leaderboard, many=True)
    return Response(serializer.data)
