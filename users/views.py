from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
import cloudinary
import cloudinary.uploader

User = get_user_model()

    

@swagger_auto_schema(methods=['POST'], request_body=UserSerializer())
@api_view(['POST'])
def signup(request):
    
    """ Allows the user to be able to sign up on the platform """

    if request.method == 'POST':
        
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():
            
            #hash password
            serializer.validated_data['password'] = make_password(serializer.validated_data['password']) #hash the given password
            User.objects.create(**serializer.validated_data)
            
            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
 
 

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=UserSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """Allows the logged in user to view their profile, edit or deactivate account. Do not use this view for changing password or resetting password"""
    
    try:
        user = User.objects.get(id = request.user.id, is_active=True)
    
    except User.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the profile of the user
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data, partial=True) 

        if serializer.is_valid():
            
            
            #upload profile picture
            if 'image' in serializer.validated_data.keys():
                try:
                    image = serializer.validated_data['image'] #get the image file from the request 
                    img1 = cloudinary.uploader.upload(image, folder = 'profile_pictures/') #upload the image to cloudinary
                    serializer.validated_data['image'] = "" #delete the image file
                    serializer.validated_data['image_url'] = img1['secure_url'] #save the image url 
                    
                except Exception:
                    data = {
                        'status'  : False,
                        'error' : "Unable to upload profile picture"
                    }

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    #delete the account
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
                'status'  : True,
                'message' : "success"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)
           
    
    
    
    
    
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='user@email.com'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view([ 'POST'])
def user_login(request):
    
    """Allows users to log in to the platform. Sends the jwt refresh and access tokens. Check settings for token life time."""
    
    if request.method == "POST":
        user = authenticate(request, username = request.data['username'], password = request.data['password'])
        if user is not None:
            if user.is_active==True:
                try:
                    refresh = RefreshToken.for_user(user)

                    user_detail = {}
                    user_detail['id']   = user.id
                    user_detail['first_name'] = user.first_name
                    user_detail['last_name'] = user.last_name
                    user_detail['username'] = user.username
                    user_detail['email'] = user.email
                    user_detail['phone'] = user.phone
                    user_detail['access'] = str(refresh.access_token)
                    user_detail['refresh'] = str(refresh)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                    'status'  : True,
                    'message' : "Successful",
                    'data' : user_detail,
                    }
                    return Response(data, status=status.HTTP_200_OK)
                

                except Exception as e:
                    raise e
                
            else:
                data = {
                'status'  : False,
                'error': 'This account has not been activated'
                }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        else:
            data = {
                'status'  : False,
                'error': 'Please provide a valid email and a password'
                }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)