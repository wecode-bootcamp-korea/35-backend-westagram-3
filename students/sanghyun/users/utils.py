import jwt
import json

from django.http        import JsonResponse
from users.models            import User
from my_settings import SECRET_KEY, ALGORITHM

def LoginConfirm(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            if 'Authorization' not in request.headers:
                return JsonResponse({"message" : "header에 Authorization이 없어"}, status = 401)
            
            access_token = request.headers.get('Authorization')           
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user_id      = payload['id']
         
            if not User.objects.filter(id = user_id).exists():
                return JsonResponse({"message" : "INVALID_UESR"}, status = 401)

            user         = User.objects.get(id = user_id)
            request.user = user

            return func(self, request, *args, **kwargs)
        
        except jwt.exceptions.DecodeError as e:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR IN DECO"}, status = 400)

    return wrapper



# class LoginConfirm:
#     def __init__(self, original_function):
#         self.original_function = original_function

#     def __call__(self, request, *args, **kwargs):
#         token = request.headers.get("Authorization", None)
#         try:
#             if token:
#                 payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
#                 user          = User.objects.get(id=payload['id'])
#                 request.user  = user
#                 return self.original_function(self, request, *args, **kwargs)

#             return JsonResponse({'messaege':'NEED_LOGIN'}, status=401)

#         except jwt.ExpiredSignatureError:
#             return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)

#         except jwt.DecodeError:
#             return JsonResponse({'message':'INVALID_USER'}, status=441)

#         except User.DoesNotExist:
#             return JsonResponse({'message':'INVALID_USER'}, status=401)