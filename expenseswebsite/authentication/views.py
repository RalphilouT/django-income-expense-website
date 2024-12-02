from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email

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