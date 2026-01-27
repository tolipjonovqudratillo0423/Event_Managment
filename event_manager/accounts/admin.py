from django.contrib import admin

from accounts.models import User, VerifyCode
# Register your models here.

admin.site.register([User, VerifyCode])