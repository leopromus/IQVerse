from django.db import models
from django.contrib.auth import get_user_model

# Get the default User model
User = get_user_model()


# 📝 1. Quiz Model
class Quiz(models.Model):
    """
    Represents a quiz with title, description, and configurations.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ❓ 2. Question Model
class Question(models.Model):
    """
    Represents a question in a quiz.
    """
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    points = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.text}"


# 🅰️ 3. Choice Model
class Choice(models.Model):
    """
    Represents choices for a question.
    """
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text} - {self.text}"


# 🧑‍🎓 4. UserQuizAttempt Model
class UserQuizAttempt(models.Model):
    """
    Tracks a user's attempt at a quiz.
    """
    user = models.ForeignKey(User, related_name='quiz_attempts', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


# ✅ 5. UserAnswer Model
class UserAnswer(models.Model):
    """
    Tracks the user's selected answers for each question.
    """
    attempt = models.ForeignKey(UserQuizAttempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.text} - {self.choice.text}"


# 💬 6. Feedback Model
class Feedback(models.Model):
    """
    Provides feedback to users after quiz completion.
    """
    attempt = models.OneToOneField(UserQuizAttempt, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.attempt.user.username} - {self.attempt.quiz.title}"


# 🔗 7. Leaderboard Model
class Leaderboard(models.Model):
    """
    Tracks top scores for each quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    date_achieved = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"


# ⚙️ 8. QuizConfiguration Model
class QuizConfiguration(models.Model):
    """
    Stores settings for each quiz.
    """
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name='config')
    randomize_questions = models.BooleanField(default=False)
    max_attempts = models.PositiveIntegerField(default=1)
    passing_score = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"Config for {self.quiz.title}"


# 📢 9. Notification Model
class Notification(models.Model):
    """
    User notifications for quiz events.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"


# 🔑 10. APIKey Model
class APIKey(models.Model):
    """
    API keys for secure data access.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"API Key for {self.user.username}"
