from django.urls import path

from users.views import SignUpView, LoginView, CommentView, PostingView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/post',PostingView.as_view()),
    path('/comment',CommentView.as_view()),
]