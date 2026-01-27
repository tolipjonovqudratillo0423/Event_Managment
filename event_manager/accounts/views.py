from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from accounts.models import User, StatusChoices, VerifyCode
from accounts.serializers import EmailSerializer,CodeSerializer,RegisterSerializer,LoginSerializer
from accounts.utils import create_code,ResponseMessage,send_code,tokens
# Create your views here.

class SendCodeToEmail(APIView):
    
    serializer_class = EmailSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data = request.data)
        
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        user = User.objects.create(email = email)
        code = user.create_code()
        
        send_code(email=email,code=code)
        
        return ResponseMessage.success(F'Your code sent to {email}',tokens(user))
        

class VerifyEmailCode(APIView):
    
    serializer_class = CodeSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data = request.data)
        
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data.get('code')
        
        if len(code) < 6:
            return Response({
                'status':False,
                'message':'Your Verification Code is too short !!! '

            })
        
        try:
            verify_code = VerifyCode.objects.get(code = code)
        except:
            return ResponseMessage.error('Code is Invalid!!!')
        
        
        if VerifyCode.is_expired(verify_code):
            return ResponseMessage.error('Code expired ')
        
    
        verify_code.user.status = StatusChoices.VERIFIED
        verify_code.user.save()
        verify_code.delete()
        
        return ResponseMessage.success('Your account has been verified')


class ResendCode(APIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def post(self,request):

        user = request.user

        if self.resend_code(user):
            return ResponseMessage.success(
                message='Your Verification Code sent Successfully')
        else:
            return ResponseMessage.error(
                message='You have got unexpired code or You have already VERIFIED'
            )
        
    def resend_code(self,user):
        
        verify_code = VerifyCode.objects.filter(user = user).first()
        
        if verify_code and not verify_code.is_expired():
            return False
        if user.status == StatusChoices.VERIFIED:
            return False
        
        code = user.create_code()
        send_code(email=user.email,code=code)
        return True
    
class RegisterUser(APIView):
    
    serializer_class = RegisterSerializer   
    permission_classes = [IsAuthenticated]            
    
    def post(self, request):
        
        serializer = self.serializer_class(data = request.data)
        
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        user.username = serializer.validated_data.get('username')
        user.phone = serializer.validated_data.get('phone')
        user.bio = serializer.validated_data.get('bio')
        user.image = serializer.validated_data.get('image')
        user.set_password(serializer.validated_data.get('password'))
        user.status = StatusChoices.DONE
        user.save()
        
        return ResponseMessage.success('Your account has been created',tokens(user))
    
        
class LoginUser(APIView):
    
    serializer_class = LoginSerializer
    
    def post(self,request):
        
        serializer = self.serializer_class(data = request.data)
        
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        
        user = authenticate(request, username = username, password = password)

        if user: 
            return ResponseMessage.success(message='You entered successfully :)',data = tokens(user=user))
        return ResponseMessage.error(message='Username or Password is incorrect !!!')