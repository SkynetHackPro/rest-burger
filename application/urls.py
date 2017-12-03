from django.conf.urls import url
from django.contrib import admin

from burgershop.views import authorisation

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth', authorisation)
]
