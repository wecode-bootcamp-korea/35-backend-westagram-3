from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    pw = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'users'
