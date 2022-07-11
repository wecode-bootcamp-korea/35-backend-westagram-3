import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View

from users.models import User

from my_settings import SECRET_KEY

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        email = data['email']
        password = data['password']
        name=data['name']
        telephone=data['telephone']
        
        try:
            EMAIL_REGEX		= r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PASSWORD_REGEX	= r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message" : "Email Invalid !!!"}, status=400)
                
            if not re.match(PASSWORD_REGEX, password):
            	return JsonResponse({"message" : "Password Invalid !!!"}, status=400)
            	
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "Email Overlapped !!!"}, status=400)
                
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')
                
            User.objects.create(
                name=name,
                email=email,
                password=decoded_password,
                telephone=telephone
            )
            
            return JsonResponse({"message" : "SUCCESS"}, status=201)
            
        except KeyError:
            return JsonResponse({"message" : "Key Error !!!"}, status=400)

class LoginView(View):
    def post(self, request):
    
        try:
            data = json.loads(request.body)
            
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status=401)
            
            if not bcrypt.checkpw(data['password'].encode('utf-8'), User.objects.get(email=data['email']).password.encode("utf-8")):
                return JsonResponse({"message" : "INVALID_USER"}, status=401)
                
            token = jwt.encode({"user_id":User.objects.get(email=data['email']).id}, SECRET_KEY, algorithm="HS256")
                
            return JsonResponse({"token" : token}, status=200)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
