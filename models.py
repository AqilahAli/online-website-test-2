from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    finishes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_earned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
class Question(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('KR', 'Korean'),
    ]
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    question_text = models.TextField()
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100, blank=True)  # Optional
    option_d = models.CharField(max_length=100, blank=True)  # Optional
    correct_answer = models.CharField(max_length=1)  # Use 'A', 'B', 'C', 'D'
    language = models.CharField(max_length=2) 
    def __str__(self):
        return self.question_text

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    score = models.IntegerField()
    total_questions = models.IntegerField()  # Ensure this field is defined here
    created_at = models.DateTimeField(auto_now_add=True)