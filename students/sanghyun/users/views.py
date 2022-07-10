import json
import re

from django.http      import JsonResponse
from django.views     import View

from users.models import User


EMAIL_REGEX    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

class SignUpView(View):
    def post(self, request):
        data         = json.loads(request.body)
        try:
            password = data['password']
            email    = data['email']
            password = data['password']


            if not re.match(EMAIL_REGEX, email):
                return JsonResponse(
                    {'message' : '메일주소 확인 바랍니다.'}, status=400
                    )


            if not re.match(PASSWORD_REGEX, password):
                return JsonResponse(
                    {'message' : '비밀번호는 8글자 이상, 문자, 숫자, 특수문자 조합이어야 합니다.'}, status=400
                    )


            if User.objects.filter(email = email).exists():
                return JsonResponse(
                    {'message' : '이미 사용중인 이메일 입니다.'}, status=400
                    )


            User.objects.create(
                name          = data['name'],
                email         = data['email'],
                password      = data['password'],
                mobile_number = data['mobile_number']
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)


        except KeyError:
            return JsonResponse({'message' : 'Key_ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        data         = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']


            if not User.objects.filter(email = email, password = password).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)