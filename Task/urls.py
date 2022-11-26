from django.urls import path
from rest_framework import routers

from .views import RegisterAPIView, LoginAPIView,UserAPIView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

]

router = routers.DefaultRouter()
router.register(r'api/v1/create_user', RegisterAPIView, "create-user")
router.register(r'api/v1/login', LoginAPIView, "login-user")
router.register(r'api/v1/user', UserAPIView, "user")

urlpatterns = router.urls + format_suffix_patterns(urlpatterns)