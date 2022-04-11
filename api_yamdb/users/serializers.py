from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username',)
        model = User

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return data


class TokenSerializer(serializers.Serializer):

    class Meta:
        fields = ('token',)
        model = User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'bio', 'email', 'first_name',
            'last_name', 'role', 'username'
        )
        model = User


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User

    def validate(self, data):
        if not self.context['request'].user.is_staff:
            data['role'] = self.context['request'].user.role
        return data
