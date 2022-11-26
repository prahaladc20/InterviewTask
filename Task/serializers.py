from rest_framework import serializers

from .models import TaskUSer


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = TaskUSer
        fields = ('email', 'username', 'password')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    username = serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    email = serializers.EmailField(
        required=False,
        write_only=True
    )

    class Meta:
        model = TaskUSer
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Use the `create_task_user` method we wrote earlier to create a new user.
        print("validated_data",validated_data)
        user = TaskUSer.objects.create_task_user(**validated_data)

        return user
