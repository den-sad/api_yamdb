from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    # def validate(self, value):
    #     request = self.context.get("request")

    #     if request and hasattr(request, "data"):
    #         data = request.data
    #         username = data.get('username', None)
    #         last_name = data.get('last_name', None)
    #         email = data.get('email', None)

    #     if len(username) > 150:
    #         raise serializers.ValidationError("username too long")

    #     if len(last_name) > 150:
    #         raise serializers.ValidationError("last_name too long")

    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         pass
    #     else:
    #         raise serializers.ValidationError(
    #             'Пользователь с таким username уже существует')
    #     if not email:
    #         raise serializers.ValidationError(
    #             'Поле email обязательно')
    #     try:
    #         User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         pass
    #     else:
    #         raise serializers.ValidationError(
    #             'Пользователь с таким email уже существует')

    #     return value
