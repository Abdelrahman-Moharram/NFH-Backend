from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, Role
import re
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id']         = str(user.id)
        token['username']   = user.username
        token['full_name']  = user.full_name
        if user.role:
            token['role']   = user.role.name
        

        return token


class BaseUserSerial(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id', 'username', 'full_name']

class UserSerial(serializers.ModelSerializer):
    role   = serializers.SerializerMethodField()
    def get_role(self, obj):
        if obj.role:
            return obj.role.name
        return None
    class Meta:
        model= User
        fields=['id', 'username', 'full_name', 'role']

class UserFormSerial(serializers.ModelSerializer):
    
    class Meta:
        model= User
        fields=['username', 'full_name', 'role', 'password']


    @property
    def is_update(self):
        return self.instance is not None
    
         
    
    def validate_username(self, value):
        value = value.strip()


        if not self.is_update and User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username already exists with another user')
        return value
    

    def save(self, **kwargs):        
        return super().save(**kwargs)