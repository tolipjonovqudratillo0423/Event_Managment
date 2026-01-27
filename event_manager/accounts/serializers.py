from rest_framework import serializers
from django.contrib.auth import get_user_model

from accounts.utils import is_valid_username

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    
    def validate(self, attrs):
        email = attrs.get('email')
        
        if get_user_model().objects.filter(email = email).exists():
            raise serializers.ValidationError('Email have already exists !')
        return super().validate(attrs)
    
    
    
class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        
        code = attrs.get('code')
        if len(code) < 6:
            raise serializers.ValidationError('Code is too short')
        
        return super().validate(attrs)
  
  
    
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length = 100,write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username','password','confirm_password','phone','bio','first_name','last_name']
        
    def validate(self, attrs):
        
        username = attrs.get('username')
        
        if not is_valid_username(username):
            raise serializers.ValidationError('Username is not valid')
        
        if get_user_model().objects.filter(username = username).exists():
            raise serializers.ValidationError('Username is already exists')
        
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('Password does not match')
        
        phone = attrs.get('phone')
        
        if not phone:
            raise serializers.ValidationError('Phone number is required')
        
        if len(phone) != 13:
            raise serializers.ValidationError('Phone number is not valid')
        
        if get_user_model().objects.filter(phone = phone).exists():
            raise serializers.ValidationError('Phone number is already exists')
        
        return super().validate(attrs)  



class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 100)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not is_valid_username(username):
            raise serializers.ValidationError('Your Username was wrote incorrect!')
        
        if len(password) < 4 :
            raise serializers.ValidationError('Your Password was wrote incorrect!')
        
        return super().validate(attrs)