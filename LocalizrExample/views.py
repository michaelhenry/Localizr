from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import (
  UserAuthSerializer,
  UserLoginSerializer
  )


class UserLoginView(APIView):

  permission_classes = (AllowAny,)
  serializer_class = UserLoginSerializer

  def post(self, request, *args, **kwargs):
    
    try:
      data = request.data
      username = data.get('username')
      password = data.get('password')

      user = authenticate(
        username=username, 
        password=password)
      
      if user is not None:
        user_serializer = UserAuthSerializer(user)
        return Response(user_serializer.data)
      else:
        return Response({'detail': 'login failed.'},
          status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
      raise e
    

login_view = UserLoginView.as_view()