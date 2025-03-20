from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from movies.models import Profile
from django.contrib.auth.models import User 


@login_required
def profile(request):
    user = request.user
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=user)

    return render(request, 'movies/profile.html', {'profile': profile})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("home")



def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

