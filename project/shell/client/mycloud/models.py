from django.db import models

# Create your models here.

class USERS(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)

class SKEYS(models.Model):
    userid = models.OneToOneField(to=USERS, to_field='userid', on_delete=models.CASCADE, primary_key=True)
    sk1 = models.CharField(max_length=45)
    sk2 = models.CharField(max_length=45)
    sk3 = models.CharField(max_length=45)

class UKEYS(models.Model):
    userid = models.OneToOneField(to=USERS, to_field='userid', on_delete=models.CASCADE, primary_key=True)
    uk1 = models.CharField(max_length=45)
    uk2 = models.CharField(max_length=45)
