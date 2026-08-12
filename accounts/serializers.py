from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Username already exists."}
            )

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "picture",
            "contact_number",
            "bio",
            "location",
            "birth_date",
        )


class AccountProfileSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    picture = serializers.ImageField(required=False, allow_null=True)
    contact_number = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)

    def to_representation(self, instance):
        profile, _ = Profile.objects.get_or_create(username=instance)

        return {
            "user": UserSerializer(instance).data,
            "profile": ProfileSerializer(profile).data,
        }

    def validate(self, attrs):
        instance = self.instance

        if "username" in attrs and User.objects.exclude(pk=instance.pk).filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        if "email" in attrs and attrs["email"] and User.objects.exclude(pk=instance.pk).filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        return attrs

    def update(self, instance, validated_data):
        profile, _ = Profile.objects.get_or_create(username=instance)

        user_fields = ("username", "first_name", "last_name", "email")
        profile_fields = ("picture", "contact_number", "bio", "location", "birth_date")

        for field in user_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()

        for field in profile_fields:
            if field in validated_data:
                setattr(profile, field, validated_data[field])

        profile.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )


class LoginSerializer(TokenObtainPairSerializer):
    pass