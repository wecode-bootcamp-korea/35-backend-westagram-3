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
            User.objects.create(
                name        = data['name'],
                email       = data['email'],
                password    = data['password'],
                phoneNumber = data['phone']
            )

            emailForm = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if emailForm == User.objects.get():
                return JsonResponse({"message": "KEY_ERROR"}, status=400 )

            passwordForm = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
            if passwordForm == User.objects.get():
                return JsonResponse({"message": "KEY_ERROR"}, status=400 )

            return JsonResponse({"message": "created"}, status=201 )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)