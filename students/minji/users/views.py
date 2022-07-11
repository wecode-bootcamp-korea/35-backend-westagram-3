import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from users.models     import User

REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email=data['email']
            password=data['password']

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            decoded_password = hashed_password.decode("utf-8")

            if not bcrypt.checkpw(data["password"].encode("utf-8"), User.password.encode("utf-8")):
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "Invalid User"}, status=400)

            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({"message" : "Invalid User"}, status=400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "Email Duplicated Entry"}, status=400)

            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone']
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class LogInView(View):
    def post(self, request):

        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email'], password=data['password']):
                return JsonResponse({"message": "SUCCESS"}, status = 200)

            return JsonResponse({"message": "INVALID_USER"}, status = 401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"},status = 400)
        
        