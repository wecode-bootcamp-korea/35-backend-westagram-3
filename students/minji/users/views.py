import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from users.models     import User

from my_settings      import ALGORITHM, SECRET_KEY

REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)

            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone']

            hashed_password  = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            decoded_password = hashed_password.decode("utf-8")

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "Invalid User"}, status=400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "Invalid User"}, status=400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "Email Duplicated Entry"}, status=400)

            User.objects.create(
                name         = name,
                email        = email,
                password     = decoded_password,
                phone_number = phone_number
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class LogInView(View):
    def post(self, request):

        data     = json.loads(request.body)

        email    = data['email']
        password = data['password']


        try:
            if User.objects.filter(email = email, password=password):
                return JsonResponse({"MESSAGE": "SUCCESS"}, status = 200)

            if not bcrypt.checkpw(password.encode("utf-8"), User.objects.get(email=email).password.encode("utf-8")):
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status = 401)
            
            encoded_jwt = jwt.encode({'id':User.objects.get(email=email).id},SECRET_KEY,algorithm=ALGORITHM)
            return JsonResponse({"Token": encoded_jwt}, status = 200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status = 400)
        
        