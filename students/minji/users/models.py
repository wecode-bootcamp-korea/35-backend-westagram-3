from django.db import models

class User(models.Model):
    name        = models.CharField(max_length=20)
    email       = models.CharField(max_length=45)
    password    = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=11)

    class Meta:
        db_table = 'users'
        
# Create your models here.
