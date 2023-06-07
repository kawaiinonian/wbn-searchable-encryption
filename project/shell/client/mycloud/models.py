from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SKey(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    sk1 = models.BinaryField()
    sk2 = models.BinaryField()
    sk3 = models.BinaryField()

class UKey(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    uk1 = models.BinaryField()
    uk2 = models.BinaryField()

class UsrAuth(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    d = models.BinaryField()
    uid = models.BinaryField()
    offtok = models.BinaryField()
    class Meta:
        unique_together = (("user", "d"),)

class DocKey(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    d = models.BinaryField()
    kd = models.BinaryField()
    kdenc = models.BinaryField()
    class Meta:
        unique_together = (("user", "d"),)

class Aid(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    aid = models.BinaryField()

class Documents(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    doc = models.CharField(max_length=45)
    class Meta:
        unique_together = (("user", "doc"),)
