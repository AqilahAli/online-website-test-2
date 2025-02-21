from django.contrib import auth, messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .models import UserProfile, UserAchievement
from django.contrib.auth import logout
from .models import Question
from django.contrib.auth.password_validation import validate_password, ValidationError
from .models import Question, UserScore, UserProfile
from django.contrib.auth.models import User


# Home view
def home_view(request):
    return render(request, 'home.html')

@login_required
def user_profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_achievements = UserAchievement.objects.filter(user=request.user)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        new_birthday = request.POST.get('birthday')

        # Update username if provided and different from the current one
        if new_username and new_username != request.user.username:
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Username updated successfully!')

        # Update email if provided and different from the current one
        if new_email and new_email != request.user.email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Email updated successfully!')

        # Update password if provided
        if new_password:
            if new_password == password_confirm:
                request.user.set_password(new_password)
                request.user.save()
                # Re-login the user after password change
                auth_login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Password updated successfully!')
        else:
            messages.error(request, 'password do not match.')    

        if new_birthday:
            user_profile.birth_date = new_birthday
            user_profile.save()
            print("Saved birth date:", user_profile.birth_date)
            messages.success(request, 'Birthday updated successfully!')
        
        # Log the user out after the update
        logout(request)
        return redirect('login')  # Redirect to login page

    return render(request, 'userprofile.html', {
        'user_profile': user_profile,
        'user_achievements': user_achievements,
    })

@login_required
def reset_finishes_count_view(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.finishes_count = 0
        user_profile.save()
        messages.success(request, 'Completed lesson count has been reset to 0.')
    
        return redirect('profile')  # Redirect to the user profile page


# Frontpage view
def frontpage(request):
    return render(request, 'frontpage.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    auth.logout(request)
    messages.success(request, "Logout successful")
    return redirect('frontpage')

def signup_view(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Corrected: User model (uppercase) should be used, not lowercase 'user'
                user = User.objects.get(username=request.POST['username'])
                messages.error(request, 'Username already exists!')
                return render(request, 'signup.html')
            except User.DoesNotExist:
                # Create new user if username doesn't exist
                user = User.objects.create_user(
                    request.POST['username'], 
                    password=request.POST['password1'],
                    first_name=request.POST['name'],
                    email=request.POST['email']
                )
                auth.login(request, user)
                
                # Create the user profile
                user_profile = UserProfile.objects.create(user=user)
                user_profile.fullName = request.POST['name']
                user_profile.Email = request.POST['email']
                user_profile.save()
                
                # Redirect to home after signup
                return redirect('login')
        else:
            messages.error(request, 'Passwords should match')
            return render(request, 'signup.html')

    return render(request, 'signup.html')

# Helper function to get fixed questions based on language
def get_questions(language):
    return Question.objects.filter(language=language).order_by('id')[:3]  # Retrieves the first 3 questions per quiz ordered by ID

# Quiz view handling both displaying questions and submitting answers
@login_required
def quiz_view(request, language):
    questions = get_questions(language)

    return render(request, 'quiz_template.html', {
        'questions': questions,
        'language': language,
        'language_code': language,  # Pass the language code for the form action
        'language_title': 'English' if language == 'EN' else 'Korean',  # Set the title based on the language
    })
# Specific views for English and Korean quizzes
def englishbeginner_view(request):
    return quiz_view(request, 'EN')

def koreanbeginner_view(request):
    return quiz_view(request, 'KR')

# Result view (mainly for handling form submissions and displaying scores)
@login_required
def result_view(request, language):
    def get_language_title(lang_code):
        return dict(Question.LANGUAGE_CHOICES).get(lang_code, 'Unknown Language')

    if request.method == "POST":
        score = 0
        total_questions = 0
        user_answers = {}

        # Retrieve all questions for the given language
        questions = Question.objects.filter(language=language)

        # Iterate through the posted answers
        for key, answer in request.POST.items():
            if key.startswith("answer_"):
                question_index = int(key.split("_")[1])  # Get the index of the question
                try:
                    question = questions[question_index]  # Adjust based on the passed language
                    total_questions += 1
                    user_answers[question.id] = answer  # Store the user's answer

                    # Check if the answer is correct
                    if question.correct_answer == answer:
                        score += 1
                except IndexError:
                    continue  # Skip if the index is out of range

        # Save score if user is authenticated
        if request.user.is_authenticated:
            UserScore.objects.create(
                user=request.user,
                language=language,
                score=score,
                total_questions=total_questions
            )

             # Increment the number of completed quizzes for the user
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.finishes_count += 1
            user_profile.save()

        # Pass user_answers and questions to the template
        return render(request, 'result.html', {
            'score': score,
            'total_questions': total_questions,
            'user_answers': user_answers,
            'questions': questions,  # Pass the entire questions queryset
            'language_title': get_language_title(language),  # Get title from the function
            'language': language  # Pass the language to the template
        })

    return redirect('home')


