from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    telephone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
