from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError #create formats to transfer over network
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site #path to webserver
from django.urls import reverse
from .utils import token_generator

#post login
from django.contrib import auth

# Create your views here.
class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        # check if username is alphanumeric
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        
        # check if username is in database
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username is in use. choose another one'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")
    
    def post(self, request):
        # messages.success(request, "Success success")
        # Get user datas
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) <6 :
                    messages.error(request, 'Password is too short')
                    return render(request, 'authentication/register.html', context)
                
                # Database
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active= False
                user.save()

                #Email
                #path to view
                #getting domain currently on
                #relative url for verification
                #encode uuid
                #token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                domain=get_current_site(request).domain
                link=reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
                activate_url = 'http://'+ domain + link
               

                email_subject = 'Activate account'
                email_body = 'Hi ' + user.username + ', please use link for verification: ' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email]
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account created.')
                return render(request, 'authentication/login.html')

        return render(request, 'authentication/register.html')

        
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            #if already used link
            if not token_generator.check_token(user, token):
                messages.success(request, 'User already activated')
                return redirect('login')
            
            #if user not activated before
            if user.is_active:
                messages.success(request, 'User already activated')
                return redirect('login')
            
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as error:
            pass
        
        return redirect('login')
    

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        # get user data from post
        username= request.POST['username']
        password= request.POST['password']
        
        
        if username and password:
            # authenticate user
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username)
                    return redirect('expenses') 
            else:
                messages.error(request, 'Activate your account through email')
                return render(request, 'authentication/login.html')
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid username')
                return render(request, 'authentication/login.html')
            elif not User.objects.filter(password=password).exists(): 
                messages.error(request, 'Invalid password')
                return render(request, 'authentication/login.html')
                
        messages.error(request, 'please fill all fields')
        return render(request, 'authentication/login.html')
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You can been logged out")
        return redirect('login')
        
        
        



class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']

        # check if username is alphanumeric
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status=400)
        # check if username is in database

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email is in use. choose another one'}, status=409)
        return JsonResponse({'email_valid': True})