from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as django_login 
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.models import User
from .forms import SignupForm
from django.contrib.auth import logout

# Create your views here.

def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        remember_me = request.POST.get("remember_me") 

        # Check if email is already registered
        if User.objects.filter(username=email).exists():
            messages.error(request, "⚠️Email already registered!")
            return redirect("signup")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "⚠️Passwords do not match!")
            return redirect("signup")

        # Create new user
        user = User.objects.create_user(username=email, email=email, password=password1)
        user.save()
        messages.success(request, "✅Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "signup.html")








def user_login(request):  # Ensure the function name is different from "login"
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            remember_me = request.POST.get("remember_me") 

            # Authenticate using Django's built-in authentication system
            try:
                user = User.objects.get(email=email)  # Get user by email
                user = authenticate(request, username=user.username, password=password)  # Authenticate using username
            except User.DoesNotExist:
                user = None

            if user is not None:
                django_login(request, user)  # Use renamed login function to avoid conflict
                if remember_me:  
                  # Set session to expire in 30 days
                  request.session.set_expiry(30 * 24 * 60 * 60)  
                else:
                  # Default session expiry when browser closes
                  request.session.set_expiry(0)
                messages.success(request, "✅Login successful!")
                return redirect("index")  # Ensure "index" is a valid URL name
            else:
                messages.error(request, "⚠️Invalid email or password.")
                return redirect("login")  # Redirect back to login page
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})


from django.contrib.auth.hashers import make_password

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "⚠️ No account found with this email.")
            return redirect("forgot_password")

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, "⚠️ Passwords do not match!")
            return redirect("forgot_password")

        # Update password
        user.password = make_password(new_password)
        user.save()

        messages.success(request, "✅ Password reset successful! Please log in.")
        return redirect("login")

    return render(request, "forgot_password.html")


def user_logout(request):
    logout(request)  # ✅ Logs out the user
    messages.success(request, "✅ You have been logged out successfully.")
    return redirect("index")  # Redirect to index page after logout