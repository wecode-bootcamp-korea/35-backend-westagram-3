import json
import re

from django.http      import JsonResponse
from django.views     import View
from users.models     import User

REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not re.match(REGEX_EMAIL, data['email']):
                return JsonResponse({"message" : "Email Error"}, status=400)

            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({"message" : "PW Error"}, status=400)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message" : "Email Duplicate"}, status=400)

            User.objects.create(
                name        = data['name'],
                email       = data['email'],
                password    = data['password'],
                phoneNumber = data['phone']
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)