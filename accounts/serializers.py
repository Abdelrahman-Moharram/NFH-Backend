from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, Role

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



# class IncludedUserPermissionsSerial(serializers.ModelSerializer):
#     permission = serializers.SerializerMethodField()

#     def get_permission(self, obj):
#         return obj.permission.key
        
#     class Meta:
#         model= Role_Permission
#         fields=['permission']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "invalid username or password"
    }
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id']             = str(user.id)
        token['username']       = str(user.username)
        token['full_name']      = str(user.full_name)
        token['role']           = str(user.role)
        # token['permissions']    = [i.permission.key for i in Role_Permission.objects.filter(role=user.role)]


        return token


class IncludedLawyerSerial(serializers.ModelSerializer):
    full_name   = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return obj.user.full_name
    class Meta:
        model= User
        fields=['id', 'full_name']

class IncludedUserSerial(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id', 'username', 'full_name']

class IncludedRoleSerial(serializers.ModelSerializer):
    class Meta:
        model= Role
        fields=['id', 'name']

# class IncludedUserTypeSerial(serializers.ModelSerializer):
#     class Meta:
#         model= UserType
#         fields=['id', 'name']


class UserSerial(serializers.ModelSerializer):
    role        = serializers.ReadOnlyField(source='role.name')
    class Meta:
        model= User
        fields=['id', 'full_name', 'username', 'role']



class ListUserSerial(serializers.ModelSerializer):
    # role        = serializers.ReadOnlyField(source='role.name')
    class Meta:
        model= User
        fields=['id', 'full_name', 'username', 'role']
    
    def to_representation(self, instance):
    
        representation = dict()
        
        representation['id']                        = instance.id
        representation['FullName']                  = instance.full_name
        representation['Username']                  = instance.username
        representation['Role']                      = instance.role.name if instance.role else ''


        return representation
    







class DetailedUserSerial(serializers.ModelSerializer):
    # role        = serializers.ReadOnlyField(source='role')
    # role        = serializers.ReadOnlyField(source='role')
    class Meta:
        model= User
        fields=['id', 'full_name', 'username', 'role']




