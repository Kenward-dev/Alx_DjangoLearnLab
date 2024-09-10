from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('', views.HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('post/new/', views.PostCreateView.as_view(), name='creating'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='editing'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='deleting'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='viewing'),
]
