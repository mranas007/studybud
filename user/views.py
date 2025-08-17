from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .form import UserProfileForm, CustomUserCreationForm
from base.models import  User, Message

# login user
def loginView(request):
    if request.user.is_authenticated:
        return redirect('rooms')
     
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User doesn't exists.")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('rooms')  # Redirect to a success page
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'user/account/login.html')


def registerView(request):
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('rooms')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('rooms')
        else:
            messages.error(request, "Registration failed. Please try again.")
    return render(request, 'user/account/register.html', {'form': form})


# logout
def logoutUser(request):
    logout(request)
    return redirect('rooms')


# user profile
@login_required(login_url="user:login")
def profile(request):
    rooms = request.user.room_set.all()[:5]
    messages = Message.objects.filter(user=request.user)[:5]
    return render(request, 'user/account/profile.html', {'user': request.user, 'rooms': rooms, 'messages': messages})


@login_required(login_url="user:login")
def update_profile(request):
    user = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        user = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if user.is_valid():
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user:profile')
    return render(request, 'user/account/update_profile.html', {'user': user})