from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, )

    class Meta:
        model = User
        # fields = "__all__"
        fields = ['id', 'email',
                  'password', "password2", 'first_name', 'last_name']
        extra_kwargs = {
            "password": {"validators": [validate_password], "write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        validated_data.pop("password2")
        username = validated_data.get("email")
        user = User.objects.create(username=username, **validated_data)
        user.set_password(user.password)
        user.save()
        return user
        # return super().create(validated_data)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email',
                  'password', "password2", 'first_name', 'last_name']


class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ['user', "key"]
