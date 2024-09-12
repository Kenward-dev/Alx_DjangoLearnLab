from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('', views.HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('post/new/', views.PostCreateView.as_view(), name='post_form'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_editForm'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    ###########################################
    ### Patterns for comments ########
    ###########################################

    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment_list'),
    # UPDATED: Changed 'post_id' to 'pk'
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    ####### Search urls#####
    path('search/', views.search_view, name='search'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),
]