from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
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
        author = data['author']
        title = self.context['view'].kwargs.get("title_id")
        reviews = Review.objects.filter(author=author, title=title)
        if reviews and self.context['request'].method == 'POST':
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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    #genre = SlugRelatedField(
    #    slug_field='slug',
    #    many=True,
    #    queryset=Genre.objects.all()
    #)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    #category = CategorySerializer(required=False)
    #genre = GenreSerializer(required=False, many=True)
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
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title