from parent.views import ParentViewSet
from django.conf.urls import url, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'parent', ParentViewSet, basename='parent')


urlpatterns = [
    url(r'', include(router.urls)),
]