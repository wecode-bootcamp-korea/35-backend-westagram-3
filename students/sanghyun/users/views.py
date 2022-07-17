import json, re, bcrypt, jwt

from django.http      import JsonResponse
from django.views     import View

from users.utils  import LoginConfirm
from users.models import User, Post, Comment
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
            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            token = jwt.encode({'id' : user.id }, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS','token' : token}, status = 200)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


class PostingView(View):
   
    @LoginConfirm
    def post(self, request):
        try:        
            data           = json.loads(request.body)
            posted_title   = data['posted_title']
            posted_content = data['posted_content']
            posted_image   = data['posted_image']
            user           = request.user
            
            Post.objects.create(
                posted_title   = posted_title,
                posted_content = posted_content,
                posted_image   = posted_image,
                user           = user
            )

            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
    
    @LoginConfirm
    def get(self, request):
        posts = Post.objects.all()
        results = []

        for post in posts:
            fix_created_at = post.created_at.strftime("%Y-%m-%d %H")+"시"
            results.append(
                {
                    "poster"     : post.user.name,
                    "title"      : post.posted_title,
                    "content"    : post.posted_content,
                    "image_url"  : post.posted_image,   
                    "created_at" : fix_created_at
                }
            )

        return JsonResponse({"postings" : results}, status = 200)


class CommentView(View):

    @LoginConfirm
    def post(self, request):
        try:
            data    = json.loads(request.body)
            content = data['comment']
            post_id = data['post']
            user    = request.user
            post    = Post.objects.get(id=post_id)

            Comment.objects.create(
                content = content,
                post    = post,
                user    = user
            )

            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
    
    @LoginConfirm
    def get(self, request):
        comments = Comment.objects.all()
        results  = []

        for comment in comments:
            fix_created_at = comment.created_at.strftime("%Y-%m-%d %H")+"시"
            results.append(
                {
                    "posted_title" : comment.post.posted_title,
                    "commenter"    : comment.user.email,
                    "content"      : comment.content,
                    "created_at"   : fix_created_at
                }
            )
        
        return JsonResponse({"comments" : results}, status = 200)
