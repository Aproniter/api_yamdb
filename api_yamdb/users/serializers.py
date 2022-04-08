from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Не очень хорошее решение.
Представьте ситуацию:
1) Пользователь отправил мейл и юзернейм
2) Система отдала ему письмо с токеном и создала пользователя в базе с таким емейлом и юзернеймом
3) Пользователь потерял письмо
4) Пытается отправить ещё раз - а сервер ему ничего не возвращает, потому что такой емейл уже есть в базе
В качестве родительского класса нужно брать обычный сериализатор, во вьюхе использовать get_or_create"""
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
    """Сериализаторы и модели нужно называть в единственном числе"""

    class Meta:
        fields = (
            'bio', 'email', 'first_name',
            'last_name', 'role', 'username'
        )
        model = User
