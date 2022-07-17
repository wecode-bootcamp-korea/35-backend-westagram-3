from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=50)
    email         = models.CharField(max_length=100, unique=True)
    password      = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=50)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'

class Post(models.Model):
    created_at     = models.DateTimeField(auto_now_add=True)
    posted_title   = models.CharField(max_length=100)
    posted_content = models.CharField(max_length=1000, blank=True)
    posted_image   = models.CharField(max_length=800)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    content    = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post       = models.ForeignKey('Post', on_delete=models.CASCADE)
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table='comment'