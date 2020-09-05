from tutor.views import TutorViewSet
from django.conf.urls import url, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'tutor', TutorViewSet, basename='tutor')

urlpatterns = [
    url(r'', include(router.urls)),
]