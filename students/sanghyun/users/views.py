import json, re, bcrypt, jwt

from django.http      import JsonResponse
from django.views     import View

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

EMAIL_REGEX    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'


class SignUpView(View):
    def post(self, request):
        data         = json.loads(request.body)
        try:
            name          = data['name']
            email         = data['email']
            password      = data['password']
            mobile_number = data['mobile_number']

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse(
                    {'message' : 'INVALID_EMAIL'}, status=400
                    )

            if not re.match(PASSWORD_REGEX, password):
                return JsonResponse(
                    {'message' : 'INVALID_PASSWORD'}, status=400
                    )

            if User.objects.filter(email = email).exists():
                return JsonResponse(
                    {'message' : 'EMAIL_ALREADY_IN_USE'}, status=400
                    )

            hashed_password         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')

            User.objects.create(
                name          = name,
                email         = email,
                password      = decoded_hashed_password,
                mobile_number = mobile_number
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'Key_ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            token = jwt.encode({'id' : user.id }, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS','token' : token}, status = 200)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)