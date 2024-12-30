from django.urls import path 
from .import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('check-username/', views.check_username, name='check_username'),
    path('signout/',views.signout,name='signout'),
    path('createProfile/',views.createProfile,name='createProfile'),
    path('profile/',views.profile,name='profile'),
    path('profile_redirect/',views.profile_redirect,name='profile_redirect'),
    path('create_post/', views.create_post, name='create_post'),
    path('home/', views.home, name='home'),
    path('search/', views.search_user, name='search_user'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    


]