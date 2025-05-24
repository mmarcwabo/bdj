from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TribunalViewSet

router = DefaultRouter()
router.register(r'core', TribunalViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]