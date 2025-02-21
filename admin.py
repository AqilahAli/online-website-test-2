from django.contrib import admin
from .models import UserProfile, Question, UserScore, UserAchievement

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthday', 'followers', 'following', 'finishes_count')
    search_fields = ('user__username', )
    list_filter = ('birthday',)

admin.site.register(UserProfile, UserProfileAdmin)

# Register the UserProfile model
admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullName', 'Email', 'birthday', 'followers', 'following')
    search_fields = ('user__username', 'fullName', 'Email')
    list_filter = ('birthday',)

# Register the UserAchievement model
admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement_name', 'completed_date')
    search_fields = ('user__username', 'achievement_name')
    list_filter = ('completed_date',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'question_text', 'correct_answer')
    list_filter = ('language',)
    search_fields = ('question_text',)

admin.site.register(Question, QuestionAdmin)

class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'language', 'score', 'total_questions')  # Display total_questions
    list_filter = ('language',)
    search_fields = ('user__username',)  # Corrected to match user object

admin.site.register(UserScore, UserScoreAdmin)

