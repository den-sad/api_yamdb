from django.conf import settings
from django.core import mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, serializers, status,
                            viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleSlugFilter
from .permissions import (IsOwnerOrModeratorOrAdmin, isAdministrator,
                          isSuperuser)
from .rating import update_rating
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterUserSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleWriteSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        user = User.objects.filter(username=username).first()
        if user:
            if email != user.email:
                raise serializers.ValidationError(
                    {'email': 'Несоответсвие email у пользователя'})
            return Response(request.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            user = serializer.save()
            subject = 'Ваш код подтверждения для регистрации'
            message = f'Ваш код: {user.confirmation_code}'
            mail.send_mail(subject=subject,
                           message=message,
                           from_email=settings.EMAIL,
                           recipient_list=[user.email, ])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    if request.method == 'POST':
        username = request.data.get('username', None)
        confirmation_code = request.data.get('confirmation_code', None)
        if not username or not confirmation_code:
            return Response({'username': username},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=username).first()
        if user:
            if confirmation_code != str(user.confirmation_code):
                raise serializers.ValidationError(
                    {'confirmation_code': 'Неверный код подтверждения'}
                )
            token = AccessToken.for_user(user).get('jti')
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'username': username},
                        status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    permission_classes = [isAdministrator | isSuperuser]
    queryset = User.objects.all()
    lookup_field = ('username')
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username',)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    throttle_classes = (ScopedRateThrottle,)
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrModeratorOrAdmin,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)
        update_rating(title)

    def perform_update(self, serializer):
        super(ReviewViewSet, self).perform_update(serializer)
        update_rating(serializer.instance.title)

    def perform_destroy(self, instance):
        super(ReviewViewSet, self).perform_destroy(instance)
        update_rating(instance.title)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    throttle_classes = (ScopedRateThrottle,)
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrModeratorOrAdmin,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        user = self.request.user
        serializer.save(
            author=user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleSlugFilter
    permission_classes = (isAdministrator,)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleWriteSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    permission_classes = (isAdministrator,)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    permission_classes = (isAdministrator,)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (permissions.IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()
