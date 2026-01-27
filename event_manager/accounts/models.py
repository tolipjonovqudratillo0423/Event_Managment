from datetime import timedelta, datetime
from django.utils import timezone

from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

from accounts.utils import create_code
# Create your models here.
class StatusChoices(models.TextChoices):
    NEW ,VERIFIED ,DONE = (('new',"New"),('verified','Verified'),('done','Done'))


class User(AbstractUser):
    username = models.CharField(max_length=100,blank=True,null = True,unique=True)
    phone = models.CharField(max_length=13,unique=True,null=True,blank=True)
    status = models.CharField(choices=StatusChoices,default=StatusChoices.NEW)
    bio = models.TextField(blank = True,null=True)
    image = models.FileField(upload_to='user/',blank=True,null=True)

    def __str__(self):
        return self.username
    
    def create_code(self ):
        
        code = create_code()

        VerifyCode.objects.create(
            user = self,
            code = code
        )
        return code
    
    def save(self,*args,**kwargs):

        if not self.username:
            self.username = str(uuid4()).split('-')[-1]
        if not self.password:
            self.password = str(uuid4()).split('-')[-1]

        return super().save(*args,**kwargs)
    

class VerifyCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_codes')
    code = models.CharField(max_length=7)
    expired_at = models.DateTimeField()
    def __str__(self):
        return f'{self.user.username} - {self.code}' 
    
    def save(self, *args, **kwargs):
        
        self.expired_at = datetime.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expired_at