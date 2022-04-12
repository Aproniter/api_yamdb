from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ValidationError

from reviews.models import (
    User, Category, Genre, Title, Review, Comment
)


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = [
            'name',
            'year',
            'category',
            'description',
            'genre',
        ]
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if value > 10 or value < 0:
            raise serializers.ValidationError(
                'Оценка по 10-бальной шкале!'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if (
                Review.objects.filter(
                    title=title,
                    author=author
                ).exists()
            ):
                raise ValidationError(
                    'Может существовать только один отзыв!'
                )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=200
    )
    username = serializers.CharField(
        max_length=200
    )

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

    def validate(self, data):
        if not self.context['request'].user.is_staff:
            data['role'] = self.context['request'].user.role
        return data
