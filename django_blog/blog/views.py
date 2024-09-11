from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, UserProfileForm, CreatePostForm, CreateCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, DetailView, CreateView
from .models import Post, Comment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            # Save the user but do not log them in
            form.save()  

            # Redirect to login page after successful registration
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Profile view
@login_required
def profile(request):
    user_form = UserChangeForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.userprofile)

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'registration/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class HomeView(TemplateView):
    template_name = 'blog/home.html'

## Post Views
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts' 
    ordering = ['-published_date']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.author = self.request.user  
        # Set the author to the logged-in user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()
        # Returns True if the user is the author
        return self.request.user == post.author 


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/post_editForm.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()
        # Returns True if the user is the author
        return self.request.user == post.author  


#####################################################
                ## Comment Views
#####################################################
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CreateCommentForm
    template_name = 'comment/comment_create.html'
    
    # Redirect after successful comment creation
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})  

    def form_valid(self, form):
        # Set the author to the logged-in user
        form.instance.author = self.request.user  
        # Get the post being commented on
        post = get_object_or_404(Post, id=self.kwargs['post_id'])  
        # Associate the comment with the post
        form.instance.post = post  
        return super().form_valid(form)

class CommentListView(ListView):
    model = Comment
    template_name = 'comment/comment_list.html'
    context_object_name = 'comments' 
    ordering = ['-published_date']

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    context_object_name = 'comment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all comments related to the post this comment belongs to
        context['comments'] = Comment.objects.filter(post=self.object.post)
        return context



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        # Returns True if the user is the author
        return self.request.user == comment.author  

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CreateCommentForm
    template_name = 'comment/comment_update.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        comment = self.get_object()
        # Returns True if the user is the author
        return self.request.user == comment.author 