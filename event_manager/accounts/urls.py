from django.urls import path

from accounts.views import SendCodeToEmail,VerifyEmailCode,ResendCode,RegisterUser,LoginUser

urlpatterns = [
    path('send-mail/', SendCodeToEmail.as_view(), name='send-email'),
    path('verify_code/',VerifyEmailCode.as_view(),name='verify-code'),
    path('resend-code/',ResendCode.as_view(),name='resend-code'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('login/',LoginUser.as_view(), name= 'login')
]