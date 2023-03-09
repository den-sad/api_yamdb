from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User

from .exceptions import CustomValidationExeption


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class RegisterTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, min_length=1, allow_blank=False)
    confirmation_code = serializers.CharField(
        max_length=150, min_length=1, allow_blank=False)

    class Meta:
        fields = ('username', 'confirmation_code')


class RegisterUserSerializer(serializers.ModelSerializer):
    regex = '^[\\w.@+-]+\\Z'
    username = serializers.RegexField(
        regex, max_length=150, min_length=1, allow_blank=False)
    email = serializers.EmailField(max_length=254, allow_blank=False)

    def validate(self, data):
        username = data['username']
        email = data['email']

        if username.lower() == 'me':
            raise serializers.ValidationError(
                "Username me запрещен")
        user_by_username = User.objects.filter(username=username).first()
        if user_by_username:
            if user_by_username.email != email:
                raise CustomValidationExeption(
                    detail="email не соотвествует username",
                    field='email',
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            raise CustomValidationExeption(
                detail=username,
                field='username',
                status_code=status.HTTP_200_OK
            )
        user_by_email = User.objects.filter(email=email).first()
        if user_by_email and (user_by_email.username != username):
            raise CustomValidationExeption(
                detail="username не соотвествует email",
                field='username',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return data

    class Meta:
        fields = ('username', 'email')
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if 'author' not in data:
                raise serializers.ValidationError(
                    'Неизвестный автор!')
            author = data['author']
            title = self.context['view'].kwargs.get("title_id")
            reviews = Review.objects.filter(author=author, title=title)
            if reviews:
                raise serializers.ValidationError(
                    'Повторный отзыв невозможен!')
        return data

    def validate_score(self, score):
        if score < 1 or score > 10:
            raise serializers.ValidationError(
                'Оценка должна быть в интервале от 1 до 10')
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title
