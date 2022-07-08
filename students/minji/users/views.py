import json
import re

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from users.models     import User

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            emailForm = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not re.match(emailForm, data['email']):
                return JsonResponse({"message": "Email Error"}, status=400 )

            passwordForm = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
            if not re.match(passwordForm, data['password']):
                return JsonResponse({"message": "PW Error"}, status=400 )

            User.objects.create(
                name        = data['name'],
                email       = data['email'],
                password    = data['password'],
                phoneNumber = data['phone']
            )

            return JsonResponse({"message": "created"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)