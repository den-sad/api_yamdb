from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        signup,
        name='signup'
    ),
    path(
        'v1/auth/token/',
        token,
        name='token'
    ),
]
