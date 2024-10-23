from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth

# Create your views here.

class EmailValidatiponView(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, this email is already taken. Please select another one'}, status=409)
        return JsonResponse({'email_valid': True})

class UsernameValidatiponView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, this username is already taken. Please select another one'}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #GET USER DATA
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST,
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
            
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                messages.success(request, 'Congratulations! You have successfully registered')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')
        


class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            try:
                user = User.objects.get(username=username)
                # Vérifie si le mot de passe correspond
                if user.check_password(password):
                    if not user.is_active:
                        messages.error(request, 'Account is not active, please contact your administrator')
                        return render(request, 'authentication/login.html')
                    # Connecte l'utilisateur
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' + user.username + ' you are now logged in')
                    return redirect('app')
                else:
                    messages.error(request, 'Invalid credentials, try again')
            except User.DoesNotExist:
                messages.error(request, 'Invalid credentials, try again')
        else:
            messages.error(request, 'Please fill all fields')

        return render(request, 'authentication/login.html')     



class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')         