from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

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
    return render(request, 'blog/register.html', {'form': form})


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

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})
