from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "password", "bio", "profile_picture"]

    def create(self, validated_data):
        # create the user
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user(password=password, **validated_data)
        # create the auth token
        Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        data["token"] = token.key
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "bio", "profile_picture", "followers"]
        read_only_fields = ["username", "email", "followers"]


class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "bio",
            "profile_picture",
            "followers_count",
            "following_count",
            "is_following",
        ]

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.is_following(obj)
