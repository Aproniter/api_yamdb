from rest_framework import serializers


from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

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


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('bio', 'email', 'first_name', 'last_name', 'role', 'username')
        model = User
