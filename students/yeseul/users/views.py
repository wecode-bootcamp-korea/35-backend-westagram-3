import json 
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

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

        if not email or not password:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message' : 'same email exists'}, status = 400)
            
        # email validation
        email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if email_regex.match(email) == None:
            return JsonResponse({'message' : 'email validation failed'}, status = 400)
        
        # password validation(8자리 이상, 최소 하나의 문자, 하나의 숫자, 하나의 특수문자)
        password_regex = re.compile('''^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@!%*?&!"£$%^&*()_+{}:@~<>?|=[\];'#,.\/\\-])[\S]{8,}$''')
        if password_regex.match(password) == None:
            return JsonResponse({'message' : 'password validation failed'}, status = 400)

        User.objects.create(
            name         = name,
            email        = email,
            password     = password,
            phone_number = phone_number
        )
        
        return JsonResponse({'message' : 'SUCCESS'}, status = 201)


