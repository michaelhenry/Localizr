from  django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserBaseSerializer(serializers.ModelSerializer):
  user_id = serializers.SerializerMethodField()

  def get_user_id(self, obj):
    return obj.pk


class UserLoginSerializer(serializers.Serializer):
  
  username = serializers.CharField(required=True)
  password = serializers.CharField(required=True)


class UserAuthSerializer(UserBaseSerializer):

  token = serializers.SerializerMethodField()

  class Meta:
    model = get_user_model()
    fields = (
      'user_id', 
      'username', 
      'email',  
      'first_name', 
      'last_name', 
      'token',
      )

    read_only_fields =  (
      'user_id', 
      'username', 
      'first_name', 
      'last_name', 
      'email',  
      'token',
      )

  def get_token(self, obj):
    token = Token.objects.filter(user=obj).first()
    if token:
      return token.key
    return None
