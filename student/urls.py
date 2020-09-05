from student.views import StudentViewSet
from django.conf.urls import url, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'student', StudentViewSet, basename='student')


urlpatterns = [
    url(r'', include(router.urls)),
]