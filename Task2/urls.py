from django.urls import path
from rest_framework import routers

from .views import AuthenticateApi
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

]

router = routers.DefaultRouter()
router.register(r'api/v1/password_check', AuthenticateApi, "authenticate-user")

urlpatterns = router.urls + format_suffix_patterns(urlpatterns)
