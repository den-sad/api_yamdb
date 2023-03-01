from rest_framework import serializers

from reviews.models import User
from reviews.models import Comment, Review, User


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
