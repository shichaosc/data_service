"""data_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from student import urls as student_urls
from parent import urls as parent_urls
from tutor import urls as tutor_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/', include(student_urls)),
    url(r'^api/', include(parent_urls)),
    url(r'^api/', include(tutor_urls)),

]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()

from django.views.static import serve
from django.conf import settings

if not settings.DEBUG:
    urlpatterns += [url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]