from django.conf.urls import url
from django.contrib import admin

from burgershop.views import authorisation, get_menu

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth', authorisation),
    url(r'^get_menu', get_menu)
]
