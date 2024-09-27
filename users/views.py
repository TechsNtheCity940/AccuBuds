from django.contrib.auth import views as auth_views
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages

User = get_user_model()

def password_reset_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        security_answer = request.POST['security_answer']
        new_password = request.POST['new_password']
        try:
            user = User.objects.get(username=username)
            if user.security_answer == security_answer:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully!")
                return redirect('login')  # Redirect to login after success
            else:
                messages.error(request, "Incorrect security answer!")
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")
    return render(request, 'password_reset.html')