import json
import re
import bcrypt
import jwt

from django.http    import JsonResponse
from django.views   import View
from django.conf    import settings 
from pathlib        import Path

from users.models   import User

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
            
        if not re.match(REGEX_EMAIL, email):
            return JsonResponse({'message' : 'email validation failed'}, status = 400)
        
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

            db_user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            access_token = jwt.encode({'id' : db_user.id}, settings.SECRET_KEY, algorithm = settings.JWT_ALGORITHM)
            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
