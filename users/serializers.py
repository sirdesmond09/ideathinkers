from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()

# class CustomUserSerializer(UserSerializer):
#     address = serializers.ReadOnlyField()

#     class Meta(UserSerializer.Meta):
#         model=User
#         fields=['id', 'firstname', 'lastname', 'email', 'phone', 'password','how_did_you_hear_about_us', 'is_admin', 'is_active', 'identity_verification', 'has_added_address', 'added_handles', 'added_profile', 'checklist_count', 'auth_provider', 'date_joined', 'address']
        
        
class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    password = serializers.CharField(write_only=True)
    
    class Meta():
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email', 'phone', 'password', 'image','image_url','date_joined']
        





