from django.db import models

# Create your models here.

class USER(models.Model):
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)

class SKEY(models.Model):
    id = models.OneToOneField(to=USER, to_field='id', on_delete=models.CASCADE, primary_key=True)
    sk1 = models.CharField(max_length=45)
    sk2 = models.CharField(max_length=45)
    sk3 = models.CharField(max_length=45)

class UKEY(models.Model):
    id = models.OneToOneField(to=USER, to_field='id', on_delete=models.CASCADE, primary_key=True)
    uk1 = models.CharField(max_length=45)
    uk2 = models.CharField(max_length=45)

class USRAUTH(models.Model):
    id = models.ForeignKey(to=USER, to_field='id', on_delete=models.CASCADE)
    d = models.CharField(max_length=45)
    uid = models.CharField(max_length=45)
    offtok = models.CharField(max_length=45)
    class Meta:
        unique_together = (("id", "d"),)

class DOCKEY(models.Model):
    id = models.ForeignKey(to=USER, to_field='id', on_delete=models.CASCADE)
    d = models.CharField(max_length=45)
    kd = models.CharField(max_length=45)
    kdenc = models.CharField(max_length=45)
    class Meta:
        unique_together = (("id", "d"),)

class AID(models.Model):
    id = models.OneToOneField(to=USER, to_field='id', on_delete=models.CASCADE, primary_key=True)
    aid = models.CharField(max_length=45)
