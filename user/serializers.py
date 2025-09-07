from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff", "is_email_verified")
        read_only_fields = ("is_staff", "is_email_verified")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class EmailVerificationSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=100000, max_value=999999)

    def validate_code(self, value):
        user = self.context["request"].user
        if str(user.verification_code) != str(value):
            raise serializers.ValidationError(
                "Verification code does not match."
            )
        return value
