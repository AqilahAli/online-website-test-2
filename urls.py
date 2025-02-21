from django.urls import path
from . import views

urlpatterns = [
path('', views.frontpage, name='frontpage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),  
    path('home/', views.home_view, name='home'),
   path('english/', views.englishbeginner_view, name='englishbeginner'),
    path('korean/', views.koreanbeginner_view, name='koreanbeginner'),
    path('result/<str:language>/', views.result_view, name='result'),
    path('profile/', views.user_profile_view, name='profile'),
    path('reset_finishes_count/', views.reset_finishes_count_view, name='reset_finishes_count'),
]
