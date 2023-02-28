from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]
