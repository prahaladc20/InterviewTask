from rest_framework import serializers

from Task.models import TaskUSer


class Task2UserSerializer(serializers.ModelSerializer):
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
        fields = ('username', 'password')

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        user = TaskUSer.objects.get(username=data['username'])
        if not user.validiate_password(data['password']):
            raise ValueError("Invalidate user")

        return super(Task2UserSerializer, self).validate(data)