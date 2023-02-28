from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, signup, token

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet, basename='users')
#router.register(r'^users/(?P<username>\d+)', UserViewSet, basename='users')
router.register(r'users', UserViewSet, basename='users')
# router.register(
#     r'users/(?P<username>[a-z0-9]+)', UserViewSet, basename='users')

# r'^posts/(?P<id>\d+)/comments'
urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        signup,
        name='signup'
    ),
    path(
        'v1/auth/token/',
        signup,
        name='token'
    ),
]
