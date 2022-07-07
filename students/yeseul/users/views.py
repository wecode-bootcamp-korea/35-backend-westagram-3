import json 

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    # http -v POST 127.0.0.1:8000/sign_up name='영희' email='younghee@naver.com' password='1234' phone_number='01012341234'
    def post(self, request):
        data = json.loads(request.body)
        
        return JsonResponse({'results' : 1}, status = 200)