import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
                return JsonResponse({"message" : "Email Invalid !!!"}, status=400)
            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', data['password']):
            	return JsonResponse({"message" : "Password Invalid !!!"}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message" : "Email Overlapped !!!"}, status=400)
            User.objects.create(name=data['name'], email=data['email'], password=data['password'], telephone=data['telephone'])
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message" : "Key Error !!!"}, status=400)
