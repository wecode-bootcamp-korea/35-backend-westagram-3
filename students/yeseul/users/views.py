import json 
import re
import bcrypt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ObjectDoesNotExist

from users.models           import User

REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '''^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@!%*?&!"£$%^&*()_+{}:@~<>?|=[\];'#,.\/\\-])[\S]{8,}$'''

class SignUpView(View):
    def post(self, request):
        try:
            request_data = json.loads(request.body)
            name         = request_data['name']
            email        = request_data['email']
            password     = request_data['password']
            phone_number = request_data['phone_number'] 
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message' : 'same email exists'}, status = 400)
            
        # email validation
        if not re.match(REGEX_EMAIL, email):
            return JsonResponse({'message' : 'email validation failed'}, status = 400)
        
        # password validation(8자리 이상, 최소 하나의 문자, 하나의 숫자, 하나의 특수문자)
        if not re.match(REGEX_PASSWORD, password):
            return JsonResponse({'message' : 'password validation failed'}, status = 400)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

        User.objects.create(
            name         = name,
            email        = email,
            password     = hashed_password,
            phone_number = phone_number
        )
        
        return JsonResponse({'message' : 'SUCCESS'}, status = 201)

class LoginView(View):
    def post(self, request):
        try:
            request_data = json.loads(request.body)
            email        = request_data['email']
            password     = request_data['password']

            if not User.objects.filter(email=email, password=password).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        